.. _tutorial-client-side:

Step X: Client-Side Code
========================

As you may already know, that the client-side of Kaylee is written in
`CoffeeScript <http://coffeescript.org/>`. But there is nothing
what prevents you from writing the project in pure JavaScript!
Mastering the basics of CoffeeScript takes less than 10 minutes
and even without that, the project code should be simple and clear to
everybody.

The client-side code of Kaylee projects basically consists of two callbacks
in `pj` namespace: `pj.init(kl_config, app_config)` and
`pj.on_task_received (task)`. The `init` callback initializes projects (e.g.
imports 3d party libraries, setups configuration etc.). Its arguments are
global Kaylee and application configurations. It is called after the project
script is fully loaded::

  pj.init = (kl_config, app_config) ->
      importScripts(app_config.alea_script)
      pj.config = app_config
      return

Here, `alea.js` is loaded from the URL passed as the application configuration
value. The configuration is also stored to `pj.config` for later use.

The `on_task_received` callback 

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


.. _alea.js: http://baagoe.org/en/w/index.php/Better_random_numbers_for_javascript
