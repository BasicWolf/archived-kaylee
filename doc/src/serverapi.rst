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
   .. automethod:: get_action(node_id)
   .. automethod:: register(remote_host)
   .. autoattribute:: registry
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

Filters
-------

.. py:class:: kaylee.util.AutoFilterABCMeta

   The Abstract Base Metaclass which also adds auto filters functionality.
   Maintains ``auto_filter`` and ``auto_filters`` attributes of the class
   (see :ref:`auto_filters`).

   .. _api_auto_filter:

   .. py:attribute:: auto_filter

      Binary flag attribute which defines the behaviour of auto-decorating
      the class with the filters. The value is built from:

      * ``kaylee.util.NO_FILTERS``
      * ``kaylee.util.BASE_FILTERS``
      * ``kaylee.util.CONFIG_FILTERS``

      e.g. in :py:class:`Project`::

        from kaylee.util import BASE_FILTERS, CONFIG_FILTERS

        class Project(object):
            ...
            auto_filter = BASE_FILTERS | CONFIG_FILTERS

   .. _api_auto_filters:

   .. py:attribute:: auto_filters

      A ``{ 'method_name' : [filter1, ...] }`` Python dict which defines the
      filters to bound to the method::

        class Controller(object):
            ...
            auto_filters = {
               'get_task' : [app_completed_guard, ],
               'accept_result' : [normalize_result_filter, ]
            }


Controller filters
..................

.. autofunction:: kaylee.controller.app_completed_guard

.. autofunction:: kaylee.controller.normalize_result_filter

.. autofunction:: kaylee.controller.kl_result_filter

Project filters
...............

.. autofunction:: kaylee.project.ignore_null_result

.. autofunction:: kaylee.project.accepts_session_data

.. autofunction:: kaylee.project.attach_task_id_to_returned_value

