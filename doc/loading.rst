.. _loading:

Loading Kaylee
==============

This section describes the settings and various ways of loading
the Kaylee object.

.. module:: kaylee

Settings
--------

There are two ways of storing settings in Kaylee: writing them down in a
Python module or writing them in a Python class.
The "module" way is very convenient when the :py:const:`loader.SETTINGS_ENV_VAR`)
contains the path of the file::

  from kaylee.loader import SETTINGS_ENV_VAR
  os.environ[SETTINGS_ENV_VAR] = os.path.join('/path/to/kaylee/settings.py')

In this case settings are loaded automatically and can be imported anywhere::

  from kaylee import settings

The class way can be used when the module approach is not possible or settings
are constructed dynamically::

  from kaylee import Settings

  class MySettings(Settings):
      DEBUG = True

      NODES_STORAGE = {
          'name' : 'MemoryNodesRegistry',
          'config' : {
              'timeout' : '12h'
          },
      }
      ...

In this case it is also possible to setup the global settings object::

  from kaylee import settings
  settings._setup(MySettings)

Please note that although 

.. autoclass:: Settings
   :members:

