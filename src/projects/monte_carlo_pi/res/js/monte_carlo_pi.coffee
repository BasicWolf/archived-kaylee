pj =
    ALIAS : 'monte_carlo_pi'

pj.init = (kl_config, app_config) ->
    pj.config = app_config
    importScripts("#{kl_config.lib_js_root}/alea.js")

pj.on_task_recieved = (data) ->
    random = new Alea(data.id)
    counter = 0
    for i in [0..pj.config.random_points]
        x = random()
        y = random()
        if x*x + y*y <= 1
            counter += 1
    klw.task_completed({'points_in_circle' : counter})