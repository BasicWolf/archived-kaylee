pj.init = (kl_config, app_config) ->
    importScripts(app_config.alea_script)
    pj.config = app_config
    return

pj.on_task_received = (task) ->
    random = new Alea(task.id)
    counter = 0
    for i in [0..pj.config.random_points]
        x = random()
        y = random()
        if x*x + y*y <= 1
            counter += 1
    pi = 4 * counter / pj.config.random_points
    klw.task_completed({'pi' : pi})
    return