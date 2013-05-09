.. _tutorial-configuration:

Step 5: Configuring the Application
===================================

Kaylee has numerous ways of loading the configuration. The tutorial app
loads the configuration from the ``settings.py`` file.
The applications are defined in a Python dictionary-like or JSON-like
manner. First of all, the application needs a unique name and a description:

.. code-block:: python

  # settings.py

  app_mcpi = {
      'name' : 'mcpi',
      'description' : 'Find value of Pi via the Monte-Carlo method.',

      # ...
  }

Next, the project configuration (*Note, that we are still filling
the* ``app_mc_pi_1`` *dict*):

.. code-block:: python

  'project' : {
      'name' : 'MonteCarloPi',
      'config' : {
          'script' : '/static/montecarlopi/js/montecarlopi.js',
          'alea_script' : '/static/montecarlopi/js/alea.js',
          'random_points' : 1000000,
          'tasks_count' : 10
      },
  },

.. module:: kaylee

The ``name`` entry indicates the Python class (:py:class:`kaylee.Project`
subclass) used in the application. The ``config`` contains the keyword
arguments passed to ``MonteCarloPi.__init__()``.

The final piece of the configuration is the controller. To keep things
simple, let's use :py:class:`SimpleController
<kaylee.contrib.SimpleController>` from ``kaylee.contrib``. Note that this
is also the part of the application configuration and recides
inside the ``app_mc_pi_1`` dictionary:

.. code-block:: python

    'controller' : {
        'name' : 'SimpleController',

        'permanent_storage' : {
            'name' : 'MemoryPermanentStorage',
        }
    }

The ``permanent_storage`` entry defines the :py:class:`permanent storage
<PermanentStorage>` in which the results are saved. Here,
:py:class:`MemoryPermanentStorage <kaylee.contrib.MemoryPermanentStorage>`
is a simple in-memory storage from the :ref:`kaylee.contrib <contrib>`
package.

At last, the application has to be added to the :config:`APPLICATIONS`
configuration field. Please make sure that you have only the ``app_mcpi``
application in the list (this is due to the client-side demo behaviour which
picks up the first available application).
::

  APPLICATIONS = [
    app_mcpi,
  ]

Continue with  :ref:`tutorial-compiling`.
