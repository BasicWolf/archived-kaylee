.. _loading:

Loading Kaylee
==============

This section describes the settings and various ways of loading
the Kaylee object.

.. module:: kaylee


Loading the Settings
--------------------

There are two ways of loading the settings in Kaylee: loading them from a
Python module or loading them from a Python class.
The only requirement for the "module" approach is to set the
:py:const:`loader.SETTINGS_ENV_VAR` environmental variable with the path
of the settings file::

  from kaylee.loader import SETTINGS_ENV_VAR
  os.environ[SETTINGS_ENV_VAR] = os.path.join('/path/to/kaylee/settings.py')

In this case settings will be loaded automatically and can be imported
via the proxy object::

  from kaylee import settings
  print(settings.DEBUG)

In the "class" approach case you have to setup the global settings proxy
object manually::

  from kaylee import Settings # class
  from kaylee import settings # global settings proxy

  class MySettings(Settings):
      DEBUG = True

      NODES_STORAGE = {
          'name' : 'MemoryNodesRegistry',
          'config' : {
              'timeout' : '12h'
          },
      }
      ...

  settings._setup(MySettings)


Loading the Kaylee object
-------------------------

Kaylee object is loaded automatically using the configuration provided
in settings. 
