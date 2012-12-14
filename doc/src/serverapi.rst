.. _serverapi:

Server API
==========

.. module:: kaylee

This part of the documentation covers all the server-side Kaylee interfaces.


Core Objects
------------

Kaylee Object
.............

.. autoclass:: Kaylee

   .. automethod:: accept_result(node_id, result)
   .. autoattribute:: applications
   .. automethod:: clean()
   ..
      .. autoattribute:: config

   .. py:attribute:: config

      An internal configuration storage object which maintains
      the configuration initially parsed from ``**kwargs**``.
      The options are accessed as object attributes, e.g.:
      ``kl.config.WORKER_SCRIPT_URL``

   .. automethod:: get_action(node_id)
   .. automethod:: register(remote_host)
   ..
      .. autoattribute:: registry

   .. py:attribute:: registry

      Active nodes registry (an instance of :class:`NodesRegistry`).

   .. automethod:: subscribe(node_id, application)
   .. automethod:: unregister(node_id)
   .. automethod:: unsubscribe(node_id)

   .. :inherited-members:


Applications Object
...................

.. autoclass:: kaylee.core.Applications

   .. py:attribute:: names

   A list of apllications' names.


Node Objects
------------

.. autoclass:: Node
   :members:
   :inherited-members:

.. autoclass:: NodeID
   :members:
   :special-members:

.. autoclass:: NodesRegistry
   :members:

   .. automethod:: __len__
   .. automethod:: __delitem__
   .. automethod:: __getitem__
   .. automethod:: __contains__


Project Object
--------------

.. autoclass:: kaylee.Project
   :members:

   .. automethod:: __getitem__

Project modes
.............

.. autodata:: kaylee.project.AUTO_PROJECT_MODE
.. autodata:: kaylee.project.MANUAL_PROJECT_MODE

Controller Object
-----------------

.. autoclass:: Controller

   .. automethod:: accept_result(node, result)
   .. autoattribute:: completed
   .. automethod:: get_task(node)


Storage Objects
---------------

.. autoclass:: TemporalStorage
   :members:

   .. automethod:: __contains__
   .. automethod:: __delitem__
   .. automethod:: __getitem__
   .. automethod:: __len__

.. autoclass:: PermanentStorage
   :members:

   .. automethod:: __contains__
   .. automethod:: __getitem__
   .. automethod:: __iter__
   .. automethod:: __len__

.. _session_api:

Session data managers
---------------------

.. autoclass:: SessionDataManager
   :members:

.. autoclass:: kaylee.session.PhonySessionDataManager

.. autoclass:: kaylee.session.NodeSessionDataManager

.. autoclass:: kaylee.session.JSONSessionDataManager


Errors
------

.. autoclass:: kaylee.errors.KayleeError

.. autoclass:: kaylee.errors.ApplicationCompletedError

.. autoclass:: kaylee.errors.InvalidNodeIDError

.. autoclass:: kaylee.errors.InvalidResultError

.. autoclass:: kaylee.errors.NodeNotSubscribedError
   :members:

.. autoclass:: kaylee.errors.NodeRejectedError


