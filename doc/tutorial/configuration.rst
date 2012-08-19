.. _tutorial-configuration:

Step 5: Configuring the Application
===================================

Kaylee has numerous ways of loading the configuration. One of the
convenient ways is to load it from a ``.py`` file. The
``demo/demo_config.py`` file used for demo configuration can be as well used
to configure our application.
The applications are defined in a Python dictionary-like or JSON-like
manner. First of all, the application needs a unique name and a description:
::

  app_mc_pi_1 = {
      'name' : 'mc_pi.1',
      'description' : 'Find value of Pi via the Monte-Carlo method.',

      ...
  }

Now, lets add the project configuration. Note, that it is still an entry in
``app_mc_pi_1`` dict::

  'project' : {
      'name' : 'MonteCarloPiProject',
      'config' : {
          'script' : '/static/js/projects/monte_carlo_pi/monte_carlo_pi.js',
          'alea_script' : '/static/js/projects/monte_carlo_pi/alea.js',
          'random_points' : 1000000,
          'tasks_count' : 10
          },
      'storage' : {
          'name' : 'MemoryPermanentStorage',
          }
      },

.. module:: kaylee

The ``name`` entry indicated the Python class (Kaylee Project subclass) used
in this application (``MonteCarloPiProject``).
The ``config`` contains the keyword arguments passed to
``Project.__init__()``. The ``storage`` entry defines the
:py:class:`permanent storage <PermanentStorage>` to which the results are
saved. The :py:class:`MemoryPermanentStorage
<kaylee.contrib.MemoryPermanentStorage>`
is a simple in-memory storage from :ref:`kaylee.contrib <contrib>`.

The final piece of the configuration is the controller and its temporal results
storage. To keep things simple, lets use :py:class:`SimpleController
<kaylee.contrib.SimpleController>` from ``kaylee.contrib``.
Note that this is also the part of the application configuration and recides
inside the ``app_mc_pi_1`` dictionary.::

    'controller' : {
        'name' : 'SimpleController',
    }

The last step is to add the application to the :ref:`APPLICATIONS
<config-APPLICATIONS>`
configuration field. Please make sure that you have only the ``app_mc_pi_1``
application in the list (this is due to the client-side demo behaviour which
picks up the first available application).
::

  APPLICATIONS = [app_mc_pi_1 ]

That's it! You are now ready to launch the application to compute PI via
distributed calculations.


Continue with  :ref:`tutorial-running`.
