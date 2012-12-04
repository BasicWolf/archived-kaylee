_tasks_counter = 1

$(document).ready( () ->
    kl_console.init('console')
    kl_console.print('<b>Kaylee status console</b><br>')
    kl.node_registered.bind(on_node_registered)
    kl.node_subscribed.bind(on_node_subscribed)
    kl.node_unsubscibed.bind(on_node_unsubscibed)
    kl.project_imported.bind(on_project_imported)
    kl.task_received.bind(on_task_received)
    kl.task_completed.bind(on_task_completed)
    kl.result_sent.bind(on_result_sent)
    kl.log.bind(on_log)
    kl.server_error.bind(on_server_error)
    kl.register()
)

on_node_registered = (data) ->
    apps = data.applications.join(', ')
    app = data.applications[0]
    kl_console.print("Your node is registered by ID
                      <span class='cem'>#{data.node_id}</span>.")
    kl_console.print("Available applications:
                       <span class='cem'>#{apps}</span>.")
    kl_console.print("Subscribing to
                      <span class='cem'>#{app}</span>.")
    kl.subscribe(app)

on_node_subscribed = (config) ->
#    if config.__kl_project_mode__ == kl.MANUAL_PROJECT_MODE
#        kl_console.set_style(kl_console.HALF_SIZE_STYLE)
    sconfig = JSON.stringify(config, null, ' ')
    kl_console.print("Application configuration received:
                      <span class='cem'>#{sconfig}</span>.")


on_node_unsubscibed = (data) ->
    kl_console.print("Node unsubscibed: <span class='cem'>#{data}</span>")

on_project_imported = (app_name) ->
    kl_console.print("Project files imported successfully.")

on_task_received = (data) ->
    kl_console.print("Task [<span class='cem'>id=#{data.id} /
                      ##{_tasks_counter}</span>] received.")

on_task_completed = (data) ->
    kl_console.print("Task [<span class='cem'>##{_tasks_counter}</span>]
                      completed.")
    _tasks_counter += 1

on_result_sent = () ->
    kl_console.print("The result has been sent to the server.")

on_server_error = (message) ->
    kl_console.print("<span class='cerr'>SERVER ERROR: </span> #{message}")

window.onerror = (message) ->
    kl_console.print("<span class='cerr'>ERROR: </span> #{message}")

on_log = (message) ->
    kl_console.print("<span class='cem'>LOG:</span> #{message}")