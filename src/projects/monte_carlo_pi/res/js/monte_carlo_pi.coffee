alias = 'monte_carlo_pi'
kl = window.kl
pj = kl.projects[alias] = {}

pj.import = () ->
    # All further modules importing should happen here
    # when finished kl.project_imported should be triggered
    kl.node.app.start = pj.start
    kl.import_lib('alea.js', () ->
        kl.task_recieved.bind(on_task_recieved)
        kl.project_imported.trigger(alias)
    )

on_task_recieved = (task) ->
