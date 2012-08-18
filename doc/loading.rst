.. _loading:

Loading Kaylee
==============

.. module:: kaylee

Kaylee has a powerful :py:mod:`loader` module which implements several
function in order to conveniently load Kaylee and the required objects.
This part of the documentation describes how Kaylee configuration is
prepared and how Kaylee object is loaded.

Configuration
-------------
Kaylee configuration is an object which holds some config parameters.
For example: the :ref:`applications <config_APPLICATIONS>`, worker
script URI etc.

There are several ways of defining Kaylee configuration:

* Python ``dict``::

    config = {
      'AUTO_GET_ACTION' : True,
      'WORKER_SCRIPT' : '/static/js/kaylee/worker.js',
      ...
    }

* Python ``class``::

    class Config(object):
        AUTO_GET_ACTION = True
        WORKER_SCRIPT = '/static/js/kaylee/worker.js'
        ...

* Python ``module``::

    AUTO_GET_ACTION = True
    WORKER_SCRIPT = '/static/js/kaylee/worker.js'

* An absolute *path* to a Python module file.

Finally, Kaylee can be manually loaded without a configuration object
at all, but we will talk about this method a bit later.
Use the method that suits you best.


Loading Kaylee Object
---------------------

An instance of :py:class:`Kaylee` can be created based on any configuration
object described above. Kaylee object can be accessed via a global proxy
from any part of the code::

  from kaylee import kl, setup

  setup('/path/to/config/file.py') # setup accepts any valid config object

  # at this point the `kl` proxy refers to the Kaylee object.

