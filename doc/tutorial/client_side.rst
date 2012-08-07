.. _tutorial-client-side:

Step 2: Client-Side Code
========================

As you may already know, that the client-side of Kaylee is written in
`CoffeeScript <http://coffeescript.org/>`_. But there is nothing
that prevents you from writing the project in pure JavaScript!
Yet, for simplicity and clarity we are going to use CoffeeScript.
Mastering the basics of CoffeeScript takes less than 10 minutes
and even without that, the project code should be simple and clear to
everybody.

The client-side code of Kaylee projects basically consists of two callbacks
in ``pj`` namespace: :js:func:`pj.init(kl_config, app_config) <pj.init>` and
:js:func:`pj.on_task_received(task) <pj.on_task_recieved>`.
The ``pj.init()`` callback initializes projects (e.g. imports 3d party libraries,
setups configuration etc.). Its arguments are global Kaylee and application
configurations. It is called after the project script is fully loaded::

  pj.init = (kl_config, app_config) ->
      importScripts(app_config.alea_script)
      pj.config = app_config
      return

Here, ``alea.js`` is loaded from the URL passed as the application configuration
value. The configuration is also stored to ``pj.config`` for later use.

The ``on_task_received()`` callback is called every time when Kaylee
client recieves a task from the server. The ``task`` argument is the JSON object
passed from the server::

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

Here, we implement the Monte-Carlo PI algorithm and return the result via
the :js:func:`task_completed() <klw.task_completed>` function from
:ref:`Kaylee Worker API <client_workerapi>`.

If you are comfortable with the code above, just copy-paste it to
``js/monte_carlo_pi.coffee`` and be ready to move to
:ref:`tutorial-server-side`.
