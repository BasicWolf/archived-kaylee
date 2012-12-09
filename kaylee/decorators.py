from functools import wraps
from abc import ABCMeta

from .errors import ApplicationCompletedError


NO_AUTO_DECORATORS = 0x0
BASE_DECORATORS = 0x2
CONFIG_DECORATORS = 0x4


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
