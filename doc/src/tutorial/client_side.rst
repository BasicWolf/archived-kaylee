.. _tutorial-client-side:

Step 3: Client-Side Code
========================

As you may already know, the client-side of Kaylee is written in
`CoffeeScript <http://coffeescript.org/>`_. But there is nothing
that prevents you from writing the project in pure JavaScript!
Mastering the basics of CoffeeScript takes less than 30 minutes
and that is the language used in the tutorial application.

The client-side code of Kaylee projects basically consists of two callbacks
in ``pj`` namespace: :js:func:`pj.init(kl_config, app_config) <pj.init>` and
:js:func:`pj.on_task_received(task) <pj.on_task_received>`.
The ``pj.init()`` callback initializes projects (e.g. imports 3d party libraries,
setups configuration etc.). Its arguments are global Kaylee and application
configurations. It is called after the project script is fully loaded::

  pj.init = (app_config) ->
      pj.config = app_config
      kl.include(app_config.alea_script, kl.project_imported.trigger)
      return

Here, ``alea.js`` is loaded from the URL passed as the application configuration
value. The configuration is also stored to ``pj.config`` for later use.
The :js:func:`kl.project_imported` event is triggered as a successful callback
by :js:func:`kl.include` in case ``alea.js`` has been loaded successfully.
This is an important part of the project, as Kaylee is waiting for
:js:func:`kl.project_imported` to be triggered in order to continue executing
the project.

The :js:func:`process_task` callback is called every time when Kaylee client
receives a task from the server. The ``task`` argument is a JSON-formatted
task data received from the server::

  pj.process_task = (task) ->
      random = new Alea(task.id)
      counter = 0
      for i in [0..pj.config.random_points]
          x = random()
          y = random()
          if x * x + y * y <= 1
              counter += 1
      pi = 4 * counter / pj.config.random_points
      kl.task_completed.trigger({'pi' : pi})
      return

Here, the value of ``pi`` is computed via the the Monte-Carlo algorithm.
To notify Kaylee  that the task has been completed the
:js:func:`kl.task_completed` callback with the computation results is
triggered.

If you are comfortable with the code above, copy-paste it to
``monte_carlo_pi/js/monte_carlo_pi.coffee``.


Continue with :ref:`tutorial-server-side`.
