kl = window.kl

$(document).ready( () ->
    kl.console.init('console')
    kl.console.print('<b>Kaylee status console</b><br>')
    kl.node_registered.bind(on_node_registered)
    kl.node_subscribed.bind(on_node_subscribed)
    kl.start()
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

on_node_subscribed = (data) ->
    sconfig = JSON.stringify(data, null, ' ')
    kl.console.print("Application configuration recieved:
                      <span class='cem'>#{sconfig}</span>")
