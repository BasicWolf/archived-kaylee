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
   .. automethod:: subscribe(node)


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


.. _fitlers_api:

Decorators
----------

.. py:class:: kaylee.util.AutoDecoratorABCMeta

   The Abstract Base Metaclass which also adds auto decorators functionality.
   Maintains ``auto_decorator`` and ``auto_decorators`` attributes of the class
   (see :ref:`auto_decorators`).

   .. _api_auto_decorator:

   .. py:attribute:: auto_decorator

      Binary flag attribute which defines the behaviour of auto-decorating
      the class with the decorators. The value is built from:

      * ``kaylee.util.NO_DECORATORS``
      * ``kaylee.util.BASE_DECORATORS``
      * ``kaylee.util.CONFIG_DECORATORS``

      e.g. in :py:class:`Project`::

        from kaylee.util import BASE_DECORATORS, CONFIG_DECORATORS

        class Project(object):
            ...
            auto_decorator = BASE_DECORATORS | CONFIG_DECORATORS

   .. _api_auto_decorators:

   .. py:attribute:: auto_decorators

      A ``{ 'method_name' : [decorator1, ...] }`` Python dict which defines the
      decorators to bound to the method::

        class Controller(object):
            ...
            auto_decorators = {
               'get_task' : [app_completed_guard, ],
               'accept_result' : [normalize_result_decorator, ]
            }


Built-in decorators list
........................

.. autofunction:: kaylee.decorators.app_completed_guard

.. autofunction:: kaylee.decorators.normalize_result

.. autofunction:: kaylee.decorators.kl_result_handler

.. autofunction:: kaylee.decorators.ignore_none_result


.. _session_api:

Session data managers
---------------------

.. autoclass:: kaylee.session.SessionDataManager
   :members:

.. autoclass:: kaylee.session.PhonySessionDataManager

.. autoclass:: kaylee.session.NodeSessionDataManager

.. autoclass:: kaylee.session.JSONSessionDataManager
