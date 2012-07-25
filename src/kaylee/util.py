import re
import inspect
import importlib
from weakref import WeakSet, WeakKeyDictionary
from datetime import timedelta
from .errors import KayleeError
from abc import ABCMeta

_timeout_regex = re.compile(r'((?P<days>\d+?)d)?\s?((?P<hours>\d+?)h)?\s?'
                            '((?P<minutes>\d+?)m)?\s?((?P<seconds>\d+?)s)?')

def parse_timedelta(s):
    match = _timeout_regex.match(s)

    try:
        time_params = {}
        for (name, param) in match.groupdict().iteritems():
            if param is not None:
                time_params[name] = int(param)
        if time_params == {}:
            raise Exception()
        return timedelta(**time_params)
    except:
        raise KayleeError('Wrong timedelta string: {}'.format(s))


def import_object(name):
    modname, objname = name.rsplit('.', 1)
    mod = importlib.import_module(modname)
    try:
        return getattr(mod, objname)
    except AttributeError:
        raise ImportError('Object {} was not found in module {}'
                          .format(objname, modname))

# TODO: kldebug should support methods
# def kldebug(f):
#     def wrapper(*args, **kwargs):
#         sargs = ', '.join(str(arg) for arg in args)
#         skwargs = ', '.join('{} = {}'.format(key, val)
#                             for key, val in kwargs.items())

#         ret = f(*args, **kwargs)
#         print('{}({}, {}) --> {}'.format(f.__name__, sargs, skwargs, ret))
#         return ret
#     return wrapper


def new_method_proxy(func):
    def inner(self, *args):
        try:
            return func(self._wrapped, *args)
        except AttributeError:
            self._setup()
            return func(self._wrapped, *args)
    return inner


class LazyObject(object):
    """
    A wrapper for another class that can be used to delay instantiation of the
    wrapped class.

    By subclassing, you have the opportunity to intercept and alter the
    instantiation.
    """
    def __init__(self):
        self._wrapped = None

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self, name, value):
        if name == "_wrapped":
            # Assign to __dict__ to avoid infinite __setattr__ loops.
            self.__dict__["_wrapped"] = value
        else:
            try:
                setattr(self._wrapped, name, value)
            except AttributeError:
                self._setup()
                setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == "_wrapped":
            raise TypeError("Cannot delete _wrapped.")
        try:
            delattr(self._wrapped, name)
        except AttributeError:
            self._setup()
            delattr(self._wrapped, name)

    def _setup(self, obj = None):
        """
        Must be implemented by sub-classes to initialise the wrapped object.

        :param obj: An optional object to wrap. Note that checking the object
                    type and wrapping it must be done in the sub class as well.
        """
        raise NotImplementedError

    # introspection support:
    __dir__ = new_method_proxy(dir)



class AutoFilterABCMeta(ABCMeta):
    def __new__(cls, name, bases, dct):
        auto_filter = dct.get('auto_filter', True)
        if auto_filter:
            # TODO: document this
            # Automatically wrap methods from auto_filters so that the user
            # does not have to worry about the common stuff.
            for attr_name, attr in dct.iteritems():
                try:
                    wrappers = cls.auto_filters[attr_name]
                    method = attr
                    for wrapper in wrappers:
                        method = wrapper(method)
                    dct[attr_name] = method
                except KeyError:
                    pass
        return super(AutoFilterABCMeta, cls).__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super(AutoFilterABCMeta, cls).__init__(name, bases, dct)
