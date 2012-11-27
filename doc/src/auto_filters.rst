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
are not normalized, the further processing and storing he data can be
compromised. That's where Kaylee Auto Filters make an appearance.

An auto filter is simply a Python decorator automatically applied to the
methods of Controllers' or Projects' sub-classes. Thus, a programmer does not
have to worry about the minor tasks described above::

  class MyController(Controller):
      @kl_result_filter
      def accept_result(self, node, data):
          # at this point data has been checked for '__kl_result__' and
          # project.normalize(data) has been already called because
          # accept_result() has been also automatically decorated
          # via kaylee.filters.normalize_result()
          ...


Configuring
-----------
Configuring filters is very easy. Just add the ``filters`` section to the
application's controller's configuration:

.. code-block:: python

  ...
  'controller' : {
      'name' : 'SimpleController',
      'filters' : {
          'accept_result' : [
                'kaylee.controller.kl_result_filter',
                'kaylee.controller.normalize_result',
          ],
      }
  }

Here, :meth:`accept_result <Controller.accept_result>` is the name
of the decorated method and both :func:`kaylee.filters.kl_result_fitler`
and :func:`kaylee.filters.normalize_result` are the filters (Python
decorators) applied to the method.


Defining in a class
-------------------

To gain the full control of the auto-filters decorating
behaviour a user has to modify the sub-class' ``auto_filter``
and ``auto_filters`` attributes' values::

  from kaylee import Project
  from kaylee.util import BASE_FILTERS, CONFIG_FILTERS

  def my_filter(f):
      ...

  class MyProject(Project):
      auto_filter = BASE_FILTERS | CONFIG_FILTERS

      auto_filters = {
          'normalize_result' : [my_filter, ],
      }

Here, :ref:`auto_filter <api_auto_filter>` is a binary-flag
attribute which defines the auto-decorating process behaviour.
The **base filters** are the filters defined in a superclass (in this
case: :attr:`Project.auto_filters`) and **config filters** are the filters
defined in configuration.
To change that behaviour the user has to modify the value of
the ``auto_filter`` attribute, e.g.::

  class MyProject(kaylee.AutoProject):
      auto_filter = CONFIG_FILTERS

The :ref:`auto_filters <api_auto_filters>` attribute defines the filters
bound to the methods of the class. In the example the
:meth:`Project.normalize_result` is decorated
by user's ``my_filter()`` and auto-decorated by
:func:`ignore_null_result <kaylee.filters.ignore_null_result>` filtes.
