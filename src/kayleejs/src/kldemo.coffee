kl = window.kl

_tasks_counter = 0

$(document).ready( () ->
    kl.setup( { url_root : '/kaylee' } )
    kl.console.init('console')
    kl.console.print('<b>Kaylee status console</b><br>')
    kl.node_registered.bind(on_node_registered)
    kl.node_subscribed.bind(on_node_subscribed)
    kl.node_stopped.bind(on_node_stopped)
    kl.project_imported.bind(on_project_imported)
    kl.task_recieved.bind(on_task_recieved)
    kl.task_completed.bind(on_task_completed)
    kl.results_sent.bind(on_results_sent)
    kl.worker_raised_error.bind(on_worker_error)
    kl.server_raised_error.bind(on_server_error)
    kl.register()
)

on_node_registered = (data) ->
    apps = data.applications.join(', ')
    app = data.applications[0]
    kl.console.print("Your node is registered by ID
                      <span class='cem'>#{data.node_id}</span>.")
    kl.console.print("Available applications:
                       <span class='cem'>#{apps}</span>.")
    kl.console.print("Subscribing to
                      <span class='cem'>#{app}</span>.")
    kl.subscribe(app)

on_node_subscribed = (config) ->
    sconfig = JSON.stringify(config, null, ' ')
    kl.console.print("Application configuration recieved:
                      <span class='cem'>#{sconfig}</span>.")

on_node_stopped = (data) ->
    kl.console.print("Node stopped: <span class='cem'>#{data}</span>.")

on_project_imported = (app_name) ->
    kl.console.print("Project files imported successfully.")

on_task_recieved = (data) ->
    kl.console.print("Task [<span class='cem'>#{data.id} /
                      ##{_tasks_counter}</span>] recieved.")

on_task_completed = (data) ->
    kl.console.print("Task [<span class='cem'>##{_tasks_counter}</span>]
                      completed.")
    _tasks_counter += 1

on_results_sent = () ->
    kl.console.print("Results sent to the server.")

on_worker_error = (e) ->
    kl.console.print("ERROR: <span class='cerr'>Line #{e.lineno} in
                      #{e.filename}: #{e.message}</span>")

on_server_error = (message) ->
    kl.console.print("ERROR: <span class='cerr'>#{message}</span>")