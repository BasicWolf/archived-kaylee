.. _tutorial-client-side:

Step 3: Client-Side Code
========================

As you may already know, the client-side of Kaylee is written in
`CoffeeScript <http://coffeescript.org/>`_. But there is nothing that
prevents you from writing the project in pure JavaScript!
The following page contains the client-side code of the tutorial app
in both CoffeeScript and JavaScript so that you can "feel the difference".
I strongly encourage you spend 30 minutes mastering the CoffeeScript if
you have never had a chance to do that before.

The client-side code of Kaylee projects basically consists of two callbacks
in ``pj`` namespace: :js:func:`pj.init(app_config) <pj.init>` and
:js:func:`pj.process_task(task) <pj.process_task>`.
The ``pj.init()`` callback initializes projects (e.g. imports 3d party
libraries, setups configuration etc.). It is called after the project client
script is fully loaded:

.. code-block:: js

  var pj = kl.pj;

  pj.init = function(app_config) {
      pj.config = app_config;
      kl.include(app_config.alea_script, kl.project_imported.trigger);
  };

The same code in CoffeeScript:

.. code-block:: coffeescript

  pj = kl.pj

  pj.init = (app_config) ->
      pj.config = app_config
      kl.include(app_config.alea_script, kl.project_imported.trigger)
      return

Here, ``alea.js`` is loaded from the URL passed as the application
configuration value. The configuration is also stored to ``pj.config``
for later use. The :js:func:`kl.project_imported` event is triggered by
:js:func:`kl.include` after the ``alea.js`` script has been loaded
successfully.

.. note:: Triggering the :js:func:`kl.project_imported` event is an
          important part of the process as Kaylee is waiting for the
          event to be triggered in order to continue communicating with
          the server-side of the project.

:js:func:`pj.process_task` is called every time Kaylee client receives
a task from the server. The ``task`` argument is a JSON-formatted task data:

.. code-block:: js

  pj.on_task_received = function(task) {
      var random = new Alea(task.id);
      var counter = 0;
      for (var i = 0; i < pj.config.random_points; i++) {
          var x = random();
          var y = random();
          if (x * x + y * y <= 1) {
              counter += 1;
          }
      }
      var pi = 4 * counter / pj.config.random_points;

      kl.task_completed({pi: pi});
  };

The same code in CoffeeScript:

.. code-block:: coffeescript

  pj.process_task = (task) ->
      random = new Alea(task.id)
      counter = 0
      for i in [0..pj.config.random_points]
          x = random()
          y = random()
          if x * x + y * y <= 1
              counter += 1
      pi = 4 * counter / pj.config.random_points

      kl.task_completed.trigger({pi: pi})
      return

Here, the value of ``pi`` is computed via the the Monte-Carlo algorithm.
To notify Kaylee  that the task has been completed the
:js:attr:`kl.task_completed` event is triggered.

If you are comfortable with the code above, copy-paste it to
``montecarlopi/client/montecarlopi.js``.

Continue with :ref:`tutorial-server-side`.
