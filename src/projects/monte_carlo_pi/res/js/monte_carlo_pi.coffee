pj = {}

pj.init = (kl_config, app_config) ->
    importScripts("#{kl_config.lib_js_root}/alea.js")
    pj.config = app_config
    return

pj.on_task_recieved = (data) ->
    random = new Alea(data.id)
    counter = 0
    for i in [0..pj.config.random_points]
        x = random()
        y = random()
        if x*x + y*y <= 1
            counter += 1
    pi = 4 * counter / pj.config.random_points
    klw.task_completed({'pi' : pi})
    return