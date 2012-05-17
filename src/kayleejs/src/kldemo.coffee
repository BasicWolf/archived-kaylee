kl = window.kl

$(document).ready( () ->
    kl.console.init('console')
    kl.console.print('<b>Kaylee status console</b><br>')
    kl.node_registered.bind(on_node_registered)
    kl.node_subscribed.bind(on_node_subscribed)
    kl.app_started.bind(on_app_started)
    kl.register()
)

on_node_registered = (data) ->
    apps = data.applications.join(', ')
    app = data.applications[0]
    kl.console.print("Your node is registered by ID:
                       <span class='cem'>#{data.nid}</span>")
    kl.console.print("Available applications:
                       <span class='cem'>#{apps}</span>")
    kl.console.print("Subscribing to application:
                       <span class='cem'>#{app}</span>")
    kl.subscribe(app)

on_node_subscribed = (config) ->
    sconfig = JSON.stringify(config, null, ' ')
    kl.console.print("Application configuration recieved:
                      <span class='cem'>#{sconfig}</span>")

on_app_started = (app_name) ->
    kl.console.print("Application started:
                      <span class='cem'>#{app_name}</span>")