.. _serverapi:

Server API
==========

.. module:: kaylee

This part of the documentation covers all the server-side interfaces of Kaylee.

Kaylee Constants
----------------

.. autodata:: SETTINGS_ENV_VAR


Kaylee Object
-------------

.. autoclass:: Kaylee

   .. automethod:: register(self, remote_host)
   .. automethod:: unregister(self, node_id)
   .. automethod:: subscribe(self, node_id, application)
   .. automethod:: unsubscribe(self, node_id)
   .. automethod:: get_action(self, node_id)
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
   :special-members:

.. autoclass:: NodesRegistry
   :members:

   .. automethod:: __len__
   .. automethod:: __delitem__
   .. automethod:: __getitem__
   .. automethod:: __contains__


Project and Task Objects
------------------------

.. autoclass:: Project
   :members:

   .. automethod:: __next__
   .. automethod:: __getitem__

.. autoclass:: Task
   :members:
..    :inherited-members:

.. autoclass:: kaylee.project.TaskMeta


Controller Object
-----------------

.. autoclass:: Controller
   :members:


Storage Objects
---------------

.. autoclass:: ControllerResultsStorage
   :members:

   .. automethod:: __contains__
   .. automethod:: __delitem__
   .. automethod:: __getitem__
   .. automethod:: __len__
   .. automethod:: __setitem__

.. autoclass:: ProjectResultsStorage
   :members:

   .. automethod:: __contains__
   .. automethod:: __delitem__
   .. automethod:: __getitem__
   .. automethod:: __iter__
   .. automethod:: __len__
   .. automethod:: __setitem__


Filters
-------

.. py:class:: kaylee.util.AutoFilterABCMeta

   The Abstract Base Metaclass which also adds auto filters functionality.
   Maintains ``auto_filter`` and ``auto_filters`` attributes of the class.

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

.. autofunction:: kaylee.controller.failed_result_filter

.. autofunction:: kaylee.controller.normalize_result_filter


Project filters
...............

.. autofunction:: kaylee.project.depleted_guard

.. autofunction:: kaylee.project.ignore_null_result
