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
#     task  : null # current task data

# CONSTANTS #
#-----------#
SESSION_DATA_ATTRIBUTE = '__kl_sd__'

WORKER_SCRIPT_URL = ((scripts) ->
    scripts = document.getElementsByTagName('script')
    script = scripts[scripts.length - 1]

    if not script.getAttribute.length?
        path = script.src

    # replace 'http://address/kaylee.js' with 'http://address/klworker.js'
    path = script.getAttribute('src', -1)
    return path[..path.lastIndexOf('/')] + 'klworker.js'
)()


kl._app = null

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
            kl._preliminary_server_error_handler
        )
        return

kl.register = () ->
    kl.api.register()
    return

kl.subscribe = (name) ->
    kl._app = {
        ## data
        name : name
        config  : null
        mode    : null # a shortcut to config.__kl_project_mode__
        worker  : null
        subscribed : false
        task : null # current task data

        ## functions
        # assigned when project is being imported
        process_task   : () -> ;
    }
    kl.api.subscribe(name)
    return

kl.get_action = () ->
    if kl._app.subscribed == true
        kl.api.get_action()
    return

kl.send_result = (data) ->
    if not data?
        kl.error('Cannot send data: the value is empty.')
    if typeof(data) != 'object'
        kl.error('The returned result is not a JS object.')
    # before sending the result, check whether app.task contains
    # session data and attach it
    if SESSION_DATA_ATTRIBUTE of kl._app.task
        data[SESSION_DATA_ATTRIBUTE] = \
            kl._app.task[SESSION_DATA_ATTRIBUTE]
    kl.api.send_result(data)
    kl._app.task = null
    return

kl._message_to_worker = (msg, data = {}) ->
    kl._app.worker.postMessage({'msg' : msg, 'data' : data})
    return

kl._preliminary_server_error_handler = (err) ->
    switch(err)
        when 'INVALID_STATE_ERR'
            @get_action() if kl._app.subscribed == true
    kl.server_error.trigger(err)
    return

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
            worker = new Worker(WORKER_SCRIPT_URL)
            app.worker = worker
            worker.onmessage = (e) ->
                worker_message_handler(e)
            worker.onerror = (e) ->
                msg = "Line #{e.lineno} in #{e.filename}: #{e.message}"
                kl.error(msg)
            kl._message_to_worker('import_project', {
                'kl_config' : kl.config,
                'app_config' : app.config,
            })

        when kl.MANUAL_PROJECT_MODE
            include_urls = [config.__kl_project_script_url__]
            if config.__kl_project_styles__
                include_urls.push(config.__kl_project_styles__)
            kl.include(include_urls,
                       () -> pj.init(app.config)
            )

        else
            kl.error('Unknown Kaylee Project mode')
    return

on_node_unsubscibed = (data) ->
    kl._app.worker?.terminate()
    kl._app = null
    kl.pj = null
    return

on_project_imported = () ->
    kl._app.subscribed = true
    switch kl._app.mode
        when kl.AUTO_PROJECT_MODE
            kl._app.process_task = (data) ->
                kl._message_to_worker('process_task', data)
        when kl.MANUAL_PROJECT_MODE
            kl._app.process_task = pj.process_task
    kl.get_action()
    return

on_action_received = (action) ->
    switch action.action
        when 'task' then kl.task_received.trigger(action.data)
        when 'unsubscribe' then kl.node_unsubscibed.trigger(action.data)
        else kl.error("Unknown action: #{action.action}")
    return

on_task_received = (task) ->
    kl._app.task = task
    kl._app.process_task(task)
    return

on_task_completed = (result) ->
    if kl._app? and kl._app.task? and kl._app.subscribed == true
        kl.send_result(result)
    return

# Kaylee worker event handlers
worker_message_handler = (event) ->
    data = event.data
    msg = data.msg
    mdata = data.data
    switch msg
        when '__kl_log__' then kl.log(mdata)
        when '__kl_error__' then kl.error(mdata)
        when 'project_imported' then kl.project_imported.trigger()
        when 'task_completed' then kl.task_completed.trigger(mdata)
    return

kl.log = (msg) ->
    console.log('Kaylee: ' + msg)
    kl.message_logged.trigger(msg)

kl.error = (msg) ->
    kl.log("ERROR: ")
    throw new kl.KayleeError(msg)

# Kaylee events
kl.node_registered = new Event(on_node_registered)
kl.node_subscribed = new Event(on_node_subscribed)
kl.node_unsubscibed = new Event(on_node_unsubscibed)
kl.project_imported = new Event(on_project_imported)
kl.action_received = new Event(on_action_received)
kl.task_received = new Event(on_task_received)
kl.task_completed = new Event(on_task_completed)
kl.result_sent = new Event()
kl.message_logged = new Event()
kl.server_error = new Event()