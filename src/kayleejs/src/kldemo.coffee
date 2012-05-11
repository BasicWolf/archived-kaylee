kl = window.kl

$(document).ready( () ->
    kl.console.init('console')
    kl.console.print('Kaylee status console')
    kl.node_registered.bind(on_node_registered)
    kl.start()
)

on_node_registered = (data) ->
    apps = data.applications.join(', ')
    app = data.applications[0]
    kl.console.print("Your node is registered by ID: <span style='color:yellow'>#{data.nid}</span>")
    kl.console.print("Available applications: <span style='color:yellow'>#{apps}</span>")
    kl.console.print("Registering for application: <span style='color:yellow'>#{app}</span>")
