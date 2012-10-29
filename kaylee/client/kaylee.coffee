###
#    kaylee.coffee
#    ~~~~~~~~~~~~~
#
#    This is the base file of Kaylee client-side module.
#
#    :copyright: (c) 2012 by Zaur Nasibov.
#    :license: MIT, see LICENSE for more details.
###

## Variables and interfaces defined in Kaylee namespace:
# kl.node_id : null

# kl._app :
#     name : null   # str
#     config : null # {}
#     worker : null # Worker object
#     subscribed : false
#     task_data  : null # current task data

kl.api =
    register : () ->
        kl.get("/kaylee/register",
                kl.node_registered.trigger,
                kl.server_error.trigger)
        return

    subscribe : (name) ->
        kl.post("/kaylee/apps/#{name}/subscribe/#{kl.node_id}",
                null,
                kl.node_subscribed.trigger,
                kl.server_error.trigger)
        return

    get_action : () ->
        kl.get("/kaylee/actions/#{kl.node_id}",
               kl.action_received.trigger,
               kl.server_error.trigger)
        return

    send_result : (result) ->
        kl.post("/kaylee/actions/#{kl.node_id}", result,
            ((action_data) ->
                kl.result_sent.trigger(result)
                kl.action_received.trigger(action_data)
            ),
            kl._default_server_error_handler
        )
        return

kl.register = () ->
    kl.api.register()
    return

kl.subscribe = (name) ->
    kl._app = {
        # data
        name : name
        config  : null
        mode    : null       # a shortcut to config.__kl_project_mode__
        worker  : null
        subscribed : false
        task_data : null     # current task data

        # functions
        process_task   : null
    }
    kl.api.subscribe(name)
    return

kl.get_action = () ->
    if kl._app.subscribed
        kl.api.get_action()
    return

kl.send_result = (data) ->
    if kl._app.subscribed
        # before sending the result, check whether app.task_data contains
        # session data and attach it
        if kl._app.task_data.__kl_tsd__?
            if (typeof(data) !== 'object')
                kl.exception.trigger('Cannot attach session data to a result
                    which is not an JS object')
                return
            data.__kl_tsd__ = kl._app.task_data.__kl_tsd__
        kl.api.send_result(data)
    return

kl._message_to_worker = (msg, data = {}) ->
    kl._app.worker.postMessage({'msg' : msg, 'data' : data})
    return

kl._default_server_error_handler = (err) ->
    switch(err)
        when 'INVALID_STATE_ERR'
            @get_action() if kl._app.subscribed
    kl.server_error.trigger(err)
    return

kl.assert = (condition, message) ->
    if condition
        kl.exception.trigger("ASSERT: #{message}")

# Primary event handlers
on_node_registered = (data) ->
    for key, val of data.config
        kl.config[key] = val
    kl.node_id = data.node_id
    return

on_node_subscribed = (config) ->
    app = kl._app
    app.config = config
    app.mode = config.__kl_project_mode__

    switch config.__kl_project_mode__
        when kl.AUTO_PROJECT_MODE
            app.worker.terminate() if app.worker?
            worker = new Worker(kl.config.WORKER_SCRIPT_URL)
            app.worker = worker
            worker.onmessage = (e) -> worker_message_handler(e)
            worker.onerror = kl.client_error.trigger
            kl._message_to_worker('import_project', {
                'kl_config' : kl.config,
                'app_config' : app.config,
            })
            app.subscribed = true

        when kl.MANUAL_PROJECT_MODE
            include_urls = [config.__kl_project_script__]
            if config.__kl_project_styles__
                include_urls.push(config.__kl_project_styles__)
            kl.include(include_urls,
                       () ->  pj.init(kl.config, app.config,
                                      kl.project_imported,
                                      kl.client_error.trigger)
            )
            app.subscribed = true

        else
            kl.exception.trigger('Unknown Kaylee Project mode')
    return


on_node_unsubscibed = (data) ->
    kl._app.subscribed = false
    kl._app.worker.terminate()
    kl._app.worker = null;
    return

on_project_imported = () ->
    switch kl._app.mode
        when kl.AUTO_PROJECT_MODE
            kl._app.process_task = (data) ->
                kl._message_to_worker('process_task', data)
        when kl.MANUAL_PROJECT_MODE
            kl._app.process_task = pj.process_task
    kl.get_action()
    return

on_action_received = (data) ->
    switch data.action
        when 'task' then kl.task_received.trigger(data.data)
        when 'unsubscribe' then kl.node_unsubscibed.trigger(data.data)
        else kl.exception("Unknown action: #{data.action}")
    return

on_task_received = (data) ->
    kl._app.task_data = data
    kl._app.process_task(data)
    return

on_task_completed = (data) ->
    kl.send_result(data)
    return

# Kaylee worker event handlers
worker_message_handler = (event) ->
    data = event.data
    msg = data.msg
    mdata = data.data
    switch msg
        when '__kl_log__' then kl.log.trigger(mdata)
        when '__kl_error__' then kl.client_error.trigger(mdata)
        when '__kl_assert__' then kl.assert(mdata)
        when 'project_imported' then kl.project_imported.trigger()
        when 'task_completed' then kl.task_completed.trigger(mdata)
    return

# Kaylee events
kl.node_registered = new Event(on_node_registered)
kl.node_subscribed = new Event(on_node_subscribed)
kl.node_unsubscibed = new Event(on_node_unsubscibed)
kl.project_imported = new Event(on_project_imported)
kl.action_received = new Event(on_action_received)
kl.task_received = new Event(on_task_received)
kl.task_completed = new Event(on_task_completed)
kl.result_sent = new Event()
kl.log = new Event()
kl.client_error = new Event()
kl.server_error = new Event()
kl.exception = new Event()
