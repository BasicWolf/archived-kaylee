.. _loading:

Loading Kaylee
==============

.. module:: kaylee

Kaylee has a powerful :py:mod:`loader` modules which allows loading Kaylee
and all the applications transparently to the user. This part of the
documentation describes how Kaylee settings are prepared and how Kaylee
object is loaded.

Settings
--------
Kaylee settings object holds :ref:`certain parameters <settings>` like the
applications' configurations, worker script URI etc.

There are several ways of defining Kaylee settings object:

* Python ``module``::

    AUTO_GET_ACTION = True
    WORKER_SCRIPT_URL = '/static/js/kaylee/worker.js'

* Python :class:`dict`::

    settings = {
      'AUTO_GET_ACTION' : True,
      'WORKER_SCRIPT_URL' : '/static/js/kaylee/worker.js',
      ...
    }

* Python ``class``::

    class MySettings(object):
        AUTO_GET_ACTION = True
        WORKER_SCRIPT_URL = '/static/js/kaylee/worker.js'
        ...

* An *absolute path* to a Python module.

Finally, Kaylee can be instantiated manually, but that is recommended for
testing purposes only.

.. _loading_kaylee_object:

Loading Kaylee Object
---------------------

An instance of :py:class:`Kaylee` can be created based on any settings
object described above. Kaylee object can be accessed via a global proxy
from any part of the code::

  from kaylee import kl, setup

  setup('/path/to/config/file.py') # setup accepts any valid config object

  # at this point Kaylee is loaded and the `kl` proxy refers to the
  # Kaylee object.
