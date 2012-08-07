.. _loading:

Loading Kaylee
==============

Kaylee projects rely on global ``settings`` and ``kl`` proxy objects which
correspondingly represent Kaylee settings and server instance.
This section describes how these objects are initialized and loaded.

.. module:: kaylee


Loading Settings
----------------

There are two ways of loading the settings in Kaylee: loading them from a
Python module or loading them from a Python class.
The only requirement for the "module" approach is to set the
:py:const:`loader.SETTINGS_ENV_VAR` environmental variable with the
absolute path to the settings file::

  from kaylee.loader import SETTINGS_ENV_VAR
  os.environ[SETTINGS_ENV_VAR] = os.path.join('/path/to/kaylee/settings.py')

In this case settings will be loaded automatically and can be imported
via the proxy (see :py:class:`LazyObject`) object::

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


Loading Kaylee Object
---------------------

An instance of :py:class:`Kaylee` is created automatically *after* the
settings are loaded and can be accessed via the global ``kl`` proxy::

  from kaylee import kl

  # An example Node registration handler.
  @app.route('/register')
  def register_node():
      data = kl.register(request.remote_addr)
      return json_response(data)


Quick Load
----------

The recommended way to setup both settings and Kaylee
with a single function call is::

  from kaylee import setup
  setup('/path/to/kaylee/settings.py') # or just setup(), see below

In case the environmental variable has been previously set, call ``setup()``
with no arguments.
This is generally done during the web front-end initialization, e.g.
put this code in Django project's ``models.py`` file or Flask
blueprint's/app's ``.py`` file.
