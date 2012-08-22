.. _config:

Configuration Options
=====================

This section describes Kaylee configuration options.
For information on setting up Kaylee, see :ref:`loading`.

.. config:: APPLICATIONS

APPLICATIONS
------------

The ``APPLICATIONS`` list contains the applications' configuration loaded
by Kaylee.
The format is:

.. code-block:: python

  APPLICATIONS = [
     { app1 },
     { app2 },
     { ...  }
  ]

Every ``app`` is a Python dictionary with application configuration:

.. code-block:: python

  {
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
      'filters' : { ... },
  }

  'controller' : {
      'name' : 'ControllerClassName',
      'config' : { ... },
      'filters' : { ... },
  }

Project and Controller ``config`` sections define the dictionary
which is passed as ``**kwargs`` during class initialization:

.. code-block:: python

  'config' : {
      'opt1' : 'val1',
      'opt2' : 10,
  }

The filters are defined as the following dictionary
(for more information see :ref:`auto_filters`):

.. code-block:: python

  { method_name : ["filter_function_name_1", ...] }

