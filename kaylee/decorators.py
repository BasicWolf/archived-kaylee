from functools import wraps
from abc import ABCMeta

from .errors import ApplicationCompletedError


NO_AUTO_DECORATORS = 0x0
BASE_DECORATORS = 0x2
CONFIG_DECORATORS = 0x4


#  TODO: add link to kl.NO_SOLUTION
#: The { '__kl_result__' : NO_SOLUTION } result returned by the node
#: indicates that no solution was found for the given task. The controller
#: must take this information into account (see :func:`kl_result_decorator`)
NO_SOLUTION = 0x2

#: The { '__kl_result__' : NEXT_TASK } solution returned by the node
#: indicates that the current task was simply not solved for some
#: reason, there are no results to accept and the node is asking for
#: the next task.
NEXT_TASK = 0x4

KL_RESULT = '__kl_result__'



class AutoDecoratorABCMeta(ABCMeta):
    """The Abstract Base Metaclass which also adds auto decorators
    functionality. Maintains ``auto_decorator`` and ``auto_decorators``
    attributes of the class.
    """

    def __new__(mcs, name, bases, dct):
        cls = super(AutoDecoratorABCMeta, mcs).__new__(mcs, name, bases, dct)
        if cls.auto_decorators_flags & BASE_DECORATORS:
            # wrap the methods
            for method_name, decorators in cls.auto_decorators.iteritems():
                method = getattr(cls, method_name)
                for f in decorators:
                    method = f(method)
                setattr(cls, method_name, method)
        return cls

    def __init__(mcs, name, bases, dct):
        super(AutoDecoratorABCMeta, mcs).__init__(name, bases, dct)



def app_completed_guard(f):
    """The decorator handles two cases of completed Kaylee application:

    1. First, it checks if the application has already completed and
       in that case immediately throws :exc:`ApplicationCompletedError`.
    2. Second, it wraps ``f`` in ``try..except`` block in order to
       set object's :attr:`Controller.completed` value to ``True``.
       After that :exc:`ApplicationCompletedError` is re-raised.

    *Signature*: ``(self, *args, **kwargs)``
    .. note:: This is a base decorator applied to :meth:`Controller.get_task`.
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.completed:
            raise ApplicationCompletedError(self.name)

        try:
            return f(self, *args, **kwargs)
        except ApplicationCompletedError as e:
            self.completed = True
            raise e
    return wrapper


def normalize_result(f):
    """The decorator normalizes the result before passing it further.

    *Signature*: ``(self, node, result)``

    .. note:: This is a base decorator applied to :meth:`
              Controller.accept_result`.
    """
    @wraps(f)
    def wrapper(self, node, result):
        result = self.project.normalize_result(node.task_id, result)
        return f(self, node, result)
    return wrapper


def kl_result_handler(f):
    """The decorator is designed to be used in "decision search" projects which
    imply that not every task has a correct solution, or solution exists at
    all.
    The decorator searches for ``'__kl_result__'`` key in the result and acts
    according to the bound value:

    * :data:`NO_SOLUTION` : The result passed to the decorated function is
      turned to `None`. It can be ignored by :meth:`Project.store_result`
      routine.

    *Signature*: ``(self, node, result)``
    """
    @wraps(f)
    def wrapper(self, node, result):
        try:
            kl_result = result['__kl_result__']
        except (KeyError, TypeError):
            return f(self, node, result)

        if kl_result == NO_SOLUTION:
            result = None
            return f(self, node, result)
        elif kl_result == NEXT_TASK:
            return

    return wrapper


def ignore_none_result(f):
    """Ignores the ``None`` result by **not** calling the wrapped method.

    *Signature*: ``(self, task_id, result)``

    .. note:: This is a base decorator applied to :meth:`Project.normalize_result`
              and :meth:`Controller.store_result`.
    """
    @wraps(f)
    def wrapper(self, task_id, result):
        if result is not None:
            return f(self, task_id, result)
        return None
    return wrapper
