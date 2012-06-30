.. _api:

API
===

.. module:: kaylee

This part of the documentation covers all the interfaces of Kaylee.


Kaylee Object
-------------

.. autoclass:: Kaylee

   .. automethod:: register(self, remote_host)
   .. automethod:: unregister(self, node_id)
   .. automethod:: subscribe(self, node_id, application)
   .. automethod:: unsubscribe(self, node_id)
   .. automethod:: get_task(self, node_id)
   .. automethod:: accept_result(self, node_id, data)
   .. automethod:: clean(self)
   .. :inherited-members:


Node Objects
------------

.. autoclass:: Node
   :members:
   :inherited-members:

.. autoclass:: NodeID
   :members:
   :inherited-members:
