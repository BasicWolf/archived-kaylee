kl = {
    node_id : null
    app :
        name : null   # str
        config : null # {}
        worker : null # Worker object
        subscribed : false
    classes  : {}
    config: {
        # url_root             # set by kl.setup()
        # kaylee_js_root
        # lib_js_root
        }
}

class Event
    constructor : (callback = null) ->
        @callbacks = []
        @callbacks.push(callback) if callback?

    trigger : (args...) =>
        for c in @callbacks
            c(args...)

    bind : (callback) =>
        @callbacks.push(callback)

    unbind : (callback) =>
        @callbacks[t..t] = [] if (t = @callbacks.indexOf(callback)) > -1
kl.classes.Event = Event

kl.benchmark = () ->
    return !!window.Worker

kl.setup = (config) ->
    # expected configuration
    # url_root = all Kaylee requests fill starts with current prefix
    kl.config = config

kl.register = () ->
    kl.get("#{kl.config.url_root}/register", kl.node_registered.trigger)

kl.subscribe = (app_name) ->
    kl.app.name = app_name
    kl.post("#{kl.config.url_root}/apps/#{app_name}/subscribe/#{kl.node_id}",
            {}, kl.node_subscribed.trigger
    )

kl.get_task = () ->
    kl.get("#{kl.config.url_root}/tasks/#{kl.node_id}",
           _parse_action)

kl.send_results = (data) ->
    if kl.app.subscribed
        kl.post("#{kl.config.url_root}/tasks/#{kl.node_id}", data,
            (edata) ->
                kl.results_sent.trigger()
                _parse_action(edata)
        )

_parse_action = (data) ->
    console.log(data.action)
    switch data.action
        when 'task' then kl.task_recieved.trigger(data.data)
        when 'unsubscribe' then kl.node_unsubscibed.trigger(data.data)

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

    worker = new Worker("#{kl.config.kaylee_js_root}/klworker.js");
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

on_project_imported = (args...) ->
    kl.get_task()

on_task_recieved = (data) ->
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
# TODO: add comments with signatures
kl.node_registered = new Event(on_node_registered)
kl.node_subscribed = new Event(on_node_subscribed)
kl.node_unsubscibed = new Event(on_node_unsubscibed)
kl.project_imported = new Event(on_project_imported)
kl.task_recieved = new Event(on_task_recieved)
kl.task_completed = new Event(on_task_completed)
kl.log = new Event()
kl.worker_raised_error = new Event()
kl.results_sent = new Event()
kl.server_raised_error = new Event()

window.kl = kl;