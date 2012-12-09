.. _serverapi:

Server API
==========

.. module:: kaylee

This part of the documentation covers all the server-side interfaces of Kaylee.


Kaylee Object
-------------

.. autoclass:: Kaylee

   .. automethod:: accept_result(node_id, data)
   .. autoattribute:: applications
   .. automethod:: clean()
   ..
      .. autoattribute:: config

   .. py:attribute:: config

      An instance of :class:`Config` with Kaylee configuration parsed
      from ``**kwargs``. The configuration parameters are accessed as
      follows::

        kl.config.CONFIG_PARAMETER

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


Controller Object
-----------------

.. autoclass:: Controller

   .. automethod:: accept_result(node, data)
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

.. autoclass:: kaylee.session.SessionDataManager
   :members:

.. autoclass:: kaylee.session.PhonySessionDataManager

.. autoclass:: kaylee.session.NodeSessionDataManager

.. autoclass:: kaylee.session.JSONSessionDataManager
