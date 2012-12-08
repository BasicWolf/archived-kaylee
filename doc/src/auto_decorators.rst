.. _auto_decorators:

Auto Decorators
============

.. module:: kaylee

The internal Kaylee data flows are passed through Controllers and Projects.
For example::

  class MyController(Controller):
      def accept_result(self, node, data):

          # if data['__kl_result__'] is Flase, set data to None,
          # which means that there is no need to store the data to the
          # permanent storage
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
compromised. That's where Kaylee Auto Decorators make an appearance.

An auto decorator is simply a Python decorator automatically applied to the
methods of Controllers' or Projects' sub-classes. Thus, a programmer does not
have to worry about the minor tasks described above::

  class MyController(Controller):
      @kl_result_decorator
      def accept_result(self, node, data):
          # at this point data has been checked for '__kl_result__' and
          # project.normalize(data) has been already called because
          # accept_result() has been also automatically decorated
          # via kaylee.decorators.normalize_result()
          ...


Configuring
-----------
Configuring decorators is very easy. Just add the ``decorators`` section to the
application's controller's configuration:

.. code-block:: python

  ...
  'controller' : {
      'name' : 'SimpleController',
      'decorators' : {
          'accept_result' : [
                'kaylee.controller.kl_result_handler',
                'kaylee.controller.normalize_result',
          ],
      }
  }

Here, :meth:`accept_result <Controller.accept_result>` is the name
of the decorated method and both :func:`kaylee.decorators.kl_result_fitler`
and :func:`kaylee.decorators.normalize_result` are the decorators (Python
decorators) applied to the method.


Defining in a class
-------------------

To gain the full control of the auto-decorators decorating
behaviour a user has to modify the sub-class' ``auto_decorator``
and ``auto_decorators`` attributes' values::

  from kaylee import Project
  from kaylee.util import BASE_DECORATORS, CONFIG_DECORATORS

  def my_decorator(f):
      ...

  class MyProject(Project):
      auto_decorator = BASE_DECORATORS | CONFIG_DECORATORS

      auto_decorators = {
          'normalize_result' : [my_decorator, ],
      }

Here, :ref:`auto_decorator <api_auto_decorator>` is a binary-flag
attribute which defines the auto-decorating process behaviour.
The **base decorators** are the decorators defined in a superclass (in this
case: :attr:`Project.auto_decorators`) and **config decorators** are the decorators
defined in configuration.
To change that behaviour the user has to modify the value of
the ``auto_decorator`` attribute, e.g.::

  class MyProject(kaylee.AutoProject):
      auto_decorator = CONFIG_DECORATORS

The :ref:`auto_decorators <api_auto_decorators>` attribute defines the decorators
bound to the methods of the class. In the example the
:meth:`Project.normalize_result` is decorated
by user's ``my_decorator()`` and auto-decorated by
:func:`ignore_none_result <kaylee.decorators.ignore_none_result>` filtes.
