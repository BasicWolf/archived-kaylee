kl = {
    node:  { # node state
        id  : null        # str
        app : {
            name : null   # str
            config : null # {}
            start : null  # function
        }
    }
    projects : {}
    classes  : {}
    config:
        root : '/kaylee'
        jsroot : '/static/js'
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

# kl.ajax is currently using jQuery.ajax()
kl.ajax = (url, reqtype, data, success, error) ->
   $.ajax(
        url: url,
        type: reqtype
        data: data,
        dataType: 'json'
        success: (data) ->
            success(data) if success?
            #sf.status.unlock() if not data.error?
        error: (jqXHR, status_text, errorCode) ->
            if error? then error(status_text) else kl.error(status_text)
            # sf.status.error("""Connection #{status_text}.
            # Please Refresh the page and try again.""", false)
    )
    return null

kl.post = (url, data, success, error) ->
    _success = (data) ->
        if data.error? then error(data.error) else success(data)
    kl.ajax(url, 'POST', data, _success, error)
    return null

kl.get = (url, success, error) ->
    _success = (data) ->
        if data.error? then error(data.error) else success(data)
    kl.ajax(url, 'GET', {}, success, error)
    return null

kl.error = (err) ->
    alert('Kaylee has encountered an unexpected error: #{err}')
    return null

# Function imports js/css dynamically. Current backend is $script.js library:
# https://github.com/ded/script.js
kl.import = $script

kl.import_lib = (libname, callback) ->
    kl.import("#{kl.config.jsroot}/lib/#{libname}", callback)

kl.import_project = (alias) ->
    kl.import("#{kl.config.jsroot}/projects/#{alias}/#{alias}.js",
        () ->  kl.projects[alias].import()
    )

kl.register = () ->
    kl.get("#{kl.config.root}/register", kl.node_registered.trigger)

kl.subscribe = (app_name) ->
    kl.node.app.name = app_name
    kl.get("#{kl.config.root}/apps/#{app_name}/subscribe/#{kl.node.id}",
           kl.node_subscribed.trigger
    )

kl.get_task = () ->
    kl.get("#{kl.config.root}/apps/#{app_name}/#{kl.node.id}/tasks",
           (response) ->
            switch response.action
                when 'wait' then setTimeout(kl.get_task, response.args.timeout)
                when 'task' then response.task_recieved(respons.args)
    )

# primary event handlers
on_node_registered = (data) ->
    kl.node.id = data.nid

on_node_subscribed = (config) ->
    kl.node.app.config = config
    if not kl.projects[config.alias]?
        kl.import_project(config.alias)

# this event handler should be triggered by an imported project
# when import() call is finished
on_project_imported = (alias) ->
    kl.node.app.start()

# Kaylee events
# TODO: add comments with signatures
kl.node_registered = new Event(on_node_registered)
kl.node_subscribed = new Event(on_node_subscribed)
kl.project_imported = new Event(on_project_imported)
kl.app_started = new Event()
kl.task_recieved = new Event()

window.kl = kl;