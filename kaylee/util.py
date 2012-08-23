# -*- coding: utf-8 -*-
"""
    kaylee.util
    ~~~~~~~~~~~

    The module contains common Kaylee routines and classes.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

import re
import importlib
from datetime import timedelta
from abc import ABCMeta

from .errors import KayleeError


NO_FILTERS = 0x0
BASE_FILTERS = 0x2
CONFIG_FILTERS = 0x4


def parse_timedelta(s):
    try:
        match = parse_timedelta.timeout_regex.match(s)
    except AttributeError:
        parse_timedelta.timeout_regex = re.compile(
            r'((?P<days>\d+?)d)?\s?((?P<hours>\d+?)h)?\s?'
            '((?P<minutes>\d+?)m)?\s?((?P<seconds>\d+?)s)?')
        match = parse_timedelta.timeout_regex.match(s)

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
    """The Abstract Base Metaclass which also adds auto filters
    functionality. Maintains ``auto_filter`` and ``auto_filters``
    attributes of the class.
    """

    def __new__(mcs, name, bases, dct):
        cls = super(AutoFilterABCMeta, mcs).__new__(mcs, name, bases, dct)

        if cls.auto_filter & BASE_FILTERS:
            # wrap the methods
            for method_name, filters in cls.auto_filters.iteritems():
                method = getattr(cls, method_name)
                for f in filters:
                    method = f(method)
                setattr(cls, method_name, method)

        return cls

    def __init__(mcs, name, bases, dct):
        super(AutoFilterABCMeta, mcs).__init__(name, bases, dct)
