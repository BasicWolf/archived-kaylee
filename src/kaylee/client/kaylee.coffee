## Variables and interfaces defined in Kaylee namespace:
# kl.node_id : null

# kl.app :
#     name : null   # str
#     config : null # {}
#     worker : null # Worker object
#     subscribed : false

kl = {}

kl.config = {}

kl.api =
    register : () ->
        kl.get("/kaylee/register",
               kl.node_registered.trigger,
               kl.server_raised_error.trigger)

    subscribe : (app_name) ->
        kl.post("/kaylee/apps/#{app_name}/subscribe/#{kl.node_id}",
                null,
                kl.node_subscribed.trigger,
                kl.server_raised_error.trigger)

    get_action : () ->
        kl.get("/kaylee/actions/#{kl.node_id}",
               kl.action_received.trigger,
               kl.server_raised_error.trigger)

    send_results : (results) ->
        kl.post("/kaylee/actions/#{kl.node_id}", results,
            ((action_data) ->
                kl.results_sent.trigger(results)
                kl.action_received.trigger(action_data)
            ),
            ((err) =>
                kl.server_raised_error.trigger(err)
                switch(err)
                    when 'INVALID_STATE_ERR'
                        @get_action() if kl.app.subscribed
            )
        )

class Event
    constructor : (handler = null) ->
        @handlers = []
        @handlers.push(handler) if handler?

    trigger : (args...) =>
        for c in @handlers
            c(args...)

    bind : (handler) =>
        @handlers.push(handler)

    unbind : (handler) =>
        @handlers[t..t] = [] if (t = @handlers.indexOf(handler)) > -1
kl.Event = Event

kl.benchmark = () ->
    return !!window.Worker

kl.register = () ->
    kl.api.register()

kl.subscribe = (app_name) ->
    kl.app = {
        name : name
        config : null
        worker : null
        subscribed : false
    }

    kl.api.subscribe(app_name)

kl.get_action = () ->
    kl.api.get_action()

kl.send_results = (data) ->
    if kl.app.subscribed
        kl.api.send_results(data)

kl.message_to_worker = (msg, data = {}) ->
    kl.app.worker.postMessage({'msg' : msg, 'data' : data})


# Primary event handlers
on_node_registered = (data) ->
    for key, val of data.config
        kl.config[key] = val
    kl.node_id = data.node_id

on_node_subscribed = (config) ->
    kl.app.config = config
    kl.app.worker.terminate() if kl.app.worker?
    kl.app.subscribed = true

    worker = new Worker(kl.config.KAYLEE_WORKER_SCRIPT);
    kl.app.worker = worker;
    worker.addEventListener('message', ((e) -> on_worker_message(e.data)),
                            false);
    worker.addEventListener('error', ((e) -> on_worker_error(e)), false);
    kl.message_to_worker('import_project', {
        'kl_config' : kl.config,
        'app_config' : kl.app.config,
    })


on_node_unsubscibed = (data) ->
    kl.app.subscribed = false
    kl.app.worker.terminate()
    kl.app.worker = null;

on_project_imported = () ->
    kl.get_action()


on_action_received = (data) ->
    switch data.action
        when 'task' then kl.task_received.trigger(data.data)
        when 'unsubscribe' then kl.node_unsubscibed.trigger(data.data)

on_task_received = (data) ->
    kl.message_to_worker('solve_task', data)

on_task_completed = (data) ->
    kl.send_results(data)

# worker event handlers
on_worker_message = (data) ->
    msg = data.msg
    mdata = data.data
    switch msg
        when '__klw_log__' then kl.log.trigger(mdata)
        when 'project_imported' then kl.project_imported.trigger(mdata)
        when 'task_completed' then kl.task_completed.trigger(mdata)

on_worker_error = (e) ->
    kl.worker_raised_error.trigger(e)

# Kaylee events
kl.node_registered = new Event(on_node_registered)
kl.node_subscribed = new Event(on_node_subscribed)
kl.node_unsubscibed = new Event(on_node_unsubscibed)
kl.project_imported = new Event(on_project_imported)
kl.action_received = new Event(on_action_received)
kl.task_received = new Event(on_task_received)
kl.task_completed = new Event(on_task_completed)
kl.log = new Event()
kl.worker_raised_error = new Event()
kl.results_sent = new Event()
kl.server_raised_error = new Event()

window.kl = kl;