pj =
    ALIAS : 'monte_carlo_pi'

pj.init = (config) ->
    pj.config = config
    importScripts('/static/js/lib/alea.js')

pj.on_task_recieved = (data) ->
    random = new Alea(data.task.id)
    counter = 0
    for i in [0..pj.config.random_points]
        x = random()
        y = random()
        if x*x + y*y <= 1
            counter += 1
    klw.task_completed({'in_circle_points' : counter})