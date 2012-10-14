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

# kl.app :
#     name : null   # str
#     config : null # {}
#     worker : null # Worker object
#     subscribed : false

kl.AUTO_MODE = 0x2
kl.MANUAL_MODE = 0x4

kl.config = {}
# The MANUAL_MODE project's namespace.
# (Note: AUTO_MODE project namespace is defined in klworker.coffee).
kl.pj = {}

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

    send_result : (results) ->
        kl.post("/kaylee/actions/#{kl.node_id}", results,
            ((action_data) ->
                kl.result_sent.trigger(results)
                kl.action_received.trigger(action_data)
            ),
            kl._default_server_error_handler
        )
        return

kl.register = () ->
    if kl._test_node().features.worker
        kl.api.register()
    else
        kl.log("Node cannot be registered: client does not meet the "
               "requirements.")
    return

kl.subscribe = (name) ->
    kl.app = {
        name : name
        config : null
        worker : null
        subscribed : false
    }
    kl.api.subscribe(name)
    return

kl.get_action = () ->
    if kl.app.subscribed
        kl.api.get_action()
    return

kl.send_result = (data) ->
    if kl.app.subscribed
        kl.api.send_result(data)
    return

kl._message_to_worker = (msg, data = {}) ->
    kl.app.worker.postMessage({'msg' : msg, 'data' : data})
    return

kl._default_server_error_handler = (err) ->
    kl.server_error.trigger(err)
    switch(err)
        when 'INVALID_STATE_ERR'
            @get_action() if kl.app.subscribed


# Primary event handlers
on_node_registered = (data) ->
    for key, val of data.config
        kl.config[key] = val
    kl.node_id = data.node_id
    return

on_node_subscribed = (config) ->
    kl.app.config = config
    switch config.__kl_project_mode__
        when kl.AUTO_MODE
            kl.app.worker.terminate() if kl.app.worker?

            worker = new Worker(kl.config.WORKER_SCRIPT)
            kl.app.worker = worker
            worker.onmessage = (e) -> worker_message_handler(e)
            worker.onerror = kl.client_error.trigger
            kl._message_to_worker('import_project', {
                'kl_config' : kl.config,
                'app_config' : kl.app.config,
            })

            kl.app.subscribed = true

        when kl.MANUAL_MODE
            kl.include(config.__kl_project_script__,
                       () ->  pj.init(kl.config, kl.app.config,
                                      kl.project_imported,
                                      kl.client.trigger)
            )
        else
            kl.error('Unknown kaylee Project mode')
    return


on_node_unsubscibed = (data) ->
    kl.app.subscribed = false
    kl.app.worker.terminate()
    kl.app.worker = null;
    return

on_project_imported = () ->
    kl.get_action()
    return

on_action_received = (data) ->
    switch data.action
        when 'task' then kl.task_received.trigger(data.data)
        when 'unsubscribe' then kl.node_unsubscibed.trigger(data.data)
        else alert("Unknown action: #{data.action}")
    return

on_task_received = (data) ->
    kl._message_to_worker('solve_task', data)
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
        when '__klw_log__' then kl.log.trigger(mdata)
        when '__klw_error__' then kl.client_error.trigger(mdata)
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
kl.log = new Event()
kl.result_sent = new Event()
kl.error = new Event()
kl.client_error = new Event(kl.error)
kl.server_error = new Event(kl.error)