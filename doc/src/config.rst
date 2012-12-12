.. _config:

Configuration Options
=====================

.. module:: kaylee

This section describes Kaylee configuration options.
For information on setting up Kaylee, see :ref:`loading`.

.. config:: APPLICATIONS

APPLICATIONS
------------

A list which contains the applications' configurations loaded
by Kaylee. The format is:

.. code-block:: python

  APPLICATIONS = [
     app1,
     app2,
     { ...  },
  ]

Every ``app`` is a Python dictionary with application configuration:

.. code-block:: python

  app1 = {
      'name' : 'Application name',
      'description' : 'Application description',
      'project' : { ... },
      'controller' : { ... },
  },

Project and controller configuration are also Python dictionaries:

.. code-block:: python

  'project' : {
      'name' : 'ProjectClassName',
      'config' : { ...  },
  }

  'controller' : {
      'name' : 'ControllerClassName',
      'config' : { ... },
  }

Project and Controller ``config`` sections define the dictionary
which is passed as ``**kwargs`` during class initialization.

.. code-block:: python

  'config' : {
      'opt1' : 'val1',
      'opt2' : 10,
  }

.. config:: PROJECTS_DIR

PROJECTS_DIR
------------

Defines a directory in which Kaylee searches for user projects, for
example:

``/home/user/.kaylee/projects/``.


.. config:: REGISTRY

REGISTRY
--------

Python dict with :class:`Nodes Registry <NodesRegistry>` configuration.
Format::

  REGISTRY = {
      'name' : 'RegistryClassName',
      'config' : {
        # timeout format: 1d 12h 10m 5s, e.g. "12h"; "1d 10m" etc.
        'timeout' : '12h'
      },
  }


.. config:: SESSION_DATA_MANAGER

SESSION_DATA_MANAGER
--------------------

**Optional**. Defines the session data manager.

.. note:: If the option is not defined the loader loads the deafult :class:`
          Phony <kaylee.session.PhonySessionDataManager>` manager.

Format::

  SESSION_DATA_MANAGER = {
      'name' : 'SessionDataManagerClassName',
      'config' : {},
  }


.. config:: WORKER_SCRIPT_URL

WORKER_SCRIPT_URL
-----------------

Contains the absoulte URL of Kaylee Worker script, for example:

``http://exaple.com/static/js/kaylee/klworker.js``.

Rationale:

  According to `W3C's reference`_, "When the ``Worker(scriptURL)`` constructor
  is invoked, the user agent must run the following steps:

  1. Resolve the scriptURL argument relative to the entry script's **base URL**,
     when the method is invoked.

  2. ...

The *base URL* of the entry script (
``http://exaple.com/static/js/kaylee/kaylee.js``) is the domain name part
of it (``http://example.com/``). Thus it is not possible to get the
latter part of the script location (``static/js/kaylee``) without certain
code hacks.

This option is available in order to avoid any hacks required of
``kaylee.js`` to resolve ``klworker.js`` script's location.



.. _`W3C's reference`: http://www.w3.org/TR/workers/#dom-worker
