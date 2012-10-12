.. _auto_filters:

Auto Filters
============

.. module:: kaylee

The internal Kaylee data flows are passed through Controllers and Projects.
Every result received by controller is checked for consistency, validated
and normalized. For example::

    class MyController(Controller):
        def accept_result(self, node, data):

            # if the '__kl_result__' is Flase, set data to None,
            # which means that data will not be stored to the project's storage.
            try:
                if data['__kl_result__'] == False:
                    data = None
            except KeyError:
                pass

            # validate and normalize the results
            data = self.project.normalize(data)

            ...

Programmers are humans and humans forget things. For example, if the results
are not normalized, the further processing and storage of the data can be
compromised. That's where Kaylee Auto Filters make an appearance.

An auto filter is simply a Python decorator automatically applied to the
methods of Controllers' or Projects' sub-classes. Thus, a programmer does not
have to worry about the minor tasks described above.


Configuring
-----------
Configuring filters is very easy. Just add the ``filters`` section to the
application's controller's configuration:

.. code-block:: python

  ...
  'controller' : {
      'name' : 'SimpleController',
      'filters' : {
          'accept_result' : ['kaylee.controller.failed_result_filter', ] ,
      }
  }

Here, :meth:`accept_result <Controller.accept_result>` is the name
of the decorated method and :func:`kaylee.controller.failed_result_filter`
is the filter (Python decorator) applied to the method.


Defining in a class
-------------------
Let's take a look at the source code of the :class:`Project`
class::

  from util import BASE_FILTERS, CONFIG_FILTERS

  class Project(object):
      __metaclass__ = AutoFilterABCMeta

      auto_filter = BASE_FILTERS | CONFIG_FILTERS

      auto_filters = {
         '__next__' : [depleted_guard, ],
          'normalize' : [ignore_null_result, ],
          'store_result' : [ignore_null_result, ],
      }

Here, :ref:`auto_filter <api_auto_filter>` is a binary-flag attribute
which defines the auto-decorating process behaviour.
The **base filters** are the filters defined in a superclass and
**config filters** are the filters defined in configuration.
``Project`` is the base class for user projects, thereby all the projects
will be automatically decorated by ``Project.auto_filters`` and the
filters defined in config. To change that behaviour the user has to define
the ``auto_filter`` attribute with desired value, e.g.::

  class MyProject(kaylee.AutoProject):
      auto_filter = CONFIG_FILTERS

The :ref:`auto_filters <api_auto_filters>` attribute defines the filters
bound to the methods of the class. In the example above both
:meth:`Project.normalize` and :meth:`Project.store_result` methods
are decorated by the :func:`ignore_null_result
<kaylee.project.ignore_null_result>` filter.
