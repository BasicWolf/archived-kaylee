import re
import inspect
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
    mod = __import__(modname)
    try:
        return getattr(mod, objname)
    except AttributeError:
        raise ImportError('Object {} was not found in module {}'
                          .format(objname, modname))


empty = object()
def new_method_proxy(func):
    def inner(self, *args):
        if self._wrapped is empty:
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
        self._wrapped = empty

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self, name, value):
        if name == "_wrapped":
            # Assign to __dict__ to avoid infinite __setattr__ loops.
            self.__dict__["_wrapped"] = value
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == "_wrapped":
            raise TypeError("Cannot delete _wrapped.")
        if self._wrapped is empty:
            self._setup()
        delattr(self._wrapped, name)

    def _setup(self):
        """
        Must be implemented by subclasses to initialise the wrapped object.
        """
        raise NotImplementedError

    # introspection support:
    __dir__ = new_method_proxy(dir)



class AutoFilterABCMeta(ABCMeta):
    def __new__(cls, name, bases, dct):
        auto_filter = dct.get('auto_filter', True)
        if auto_filter:
            # TODO: document this
            # Automatically wrap methods from _filters so that the user
            # does not have to worry about the common stuff.
            for attr_name, attr in dct.iteritems():
                try:
                    wrappers = cls._filters[attr_name]
                    method = attr
                    for wrapper in wrappers:
                        method = wrapper(method)
                    dct[attr_name] = method
                except KeyError:
                    pass
        return super(AutoFilterABCMeta, cls).__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super(AutoFilterABCMeta, cls).__init__(name, bases, dct)



""" A signal/slot implementation

File:    signal.py
Author:  Thiago Marcos P. Santos
Author:  Christopher S. Case
Author:  David H. Bronke
Created: August 28, 2008
Updated: December 12, 2011
License: MIT

"""

class Signal(object):
    def __init__(self):
        self._functions = WeakSet()
        self._methods = WeakKeyDictionary()

    def __call__(self, *args, **kargs):
        # Call handler functions
        for func in self._functions:
            func(*args, **kargs)

        # Call handler methods
        for obj, funcs in self._methods.items():
            for func in funcs:
                func(obj, *args, **kargs)

    def connect(self, slot):
        if inspect.ismethod(slot):
            if slot.__self__ not in self._methods:
                self._methods[slot.__self__] = set()

            self._methods[slot.__self__].add(slot.__func__)

        else:
            self._functions.add(slot)

    def disconnect(self, slot):
        if inspect.ismethod(slot):
            if slot.__self__ in self._methods:
                self._methods[slot.__self__].remove(slot.__func__)
        else:
            if slot in self._functions:
                self._functions.remove(slot)

    def clear(self):
        self._functions.clear()
        self._methods.clear()
