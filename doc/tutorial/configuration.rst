.. _tutorial-configuration:

Step 4: Configuring the Application
===================================

Kaylee's reads the configuration from a ``.py`` file. We can utilize the same
``src/bin/kl_demo_settings.py`` file used by the demo app to configure our
application. The applications are defined in a dict-like manner.
First of all, the application needs a unique name and a description:
::

  app_mc_pi_1 = {
      'name' : 'mc_pi.1',
      'description' : 'Find value of Pi via the Monte-Carlo method.',


      ...
  }

Now, let's add the configuration of the project for this app. Note, that
it is an entry in the ``app_mc_pi_1`` dict::

  'project' : {
      'name' : 'MonteCarloPiProject',
      'config' : {
          'script' : '/static/js/projects/monte_carlo_pi/monte_carlo_pi.js',
          'alea_script' : '/static/js/projects/monte_carlo_pi/alea.js',
          'random_points' : 1000000,
          'tasks_count' : 10
          },
      'storage' : {
          'name' : 'MemoryProjectResultsStorage',
          }
      },

The ``name`` entry indicated the Python class (Kaylee Project subclass) used
in this application (``MonteCarloPiProject``).
The ``config`` contains the keyword arguments passed to ``Project.__init__()``.
The ``storage`` entry defines the :py:class:`storage <ProjectStorage>` to which
the results are saved. The ``MemoryProjectResultsStorage`` is a simple in-memory
storage from ``kaylee.contrib``.

The final piece of the configuration is the controller and its temporal results
storage. Our choice is the
``ResultsComparatorController`` from ``kaylee.contrib`` TODO. Don't forget, this is
as well the part of the application configuration and recides inside the
``app_mc_pi_1`` dictionary.
::

    'controller' : {
        'name' : 'SimpleController',

        'storage' : {
            'name' : 'MemoryControllerResultsStorage',
            },
        },
    }

The last step is to add the application to the ``APPLICATIONS`` (TODO) config
key. Please make sure that you have only the ``app_mc_pi_1``  application in
the list (this is due to the client-side demo behaviour which picks up the
first available application).
::

  APPLICATIONS = [app_mc_pi_1 ]

That's it! You are now ready to launch the application to compute PI via
distributed calculations. Just continue to :ref:`tutorial-running`.
