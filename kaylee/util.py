# -*- coding: utf-8 -*-
"""
    kaylee.util
    ~~~~~~~~~~~

    The module contains common Kaylee routines and classes.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""
#pylint: disable-msg=W0402,W0212,R0913
#W0402: 15,0: Uses of a deprecated module 'string'
#W0212: Access to a protected member _wrapped of a client class
#R0913: random_string: Too many arguments (7/5)
###

import os
import re
import sys
import random
import string
import importlib
import contextlib
import logging
from datetime import timedelta
from .errors import KayleeError


def parse_timedelta(s):
    try:
        match = parse_timedelta.timeout_regex.match(s)
    except AttributeError:
        parse_timedelta.timeout_regex = re.compile(
            r'((?P<days>\d+?)d)?\s?((?P<hours>\d+?)h)?\s?'
            r'((?P<minutes>\d+?)m)?\s?((?P<seconds>\d+?)s)?')
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


def _new_method_proxy(func):
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

    __getattr__ = _new_method_proxy(getattr)

    def __setattr__(self, name, value):
        if name == '_wrapped':
            # Assign to __dict__ to avoid infinite __setattr__ loops.
            self.__dict__['_wrapped'] = value
        else:
            try:
                setattr(self._wrapped, name, value)
            except AttributeError:
                self._setup()
                setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == '_wrapped':
            raise TypeError('Cannot delete _wrapped.')
        try:
            delattr(self._wrapped, name)
        except AttributeError:
            self._setup()
            delattr(self._wrapped, name)

    def _setup(self, obj = None):
        """
        Must be implemented by sub-classes to initialize the wrapped object.

        :param obj: An optional object to wrap. Note that checking the object
                    type and wrapping it must be done in the sub class as well.
        """
        raise NotImplementedError

    # introspection support:
    __dir__ = _new_method_proxy(dir)


class DictAsObjectWrapper(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.iteritems():
            setattr(self, key, val)


class RecursiveDictAsObjectWrapper(object):
    def __init__(self, **kwargs):
        def _update(obj, d):
            for key, val in d.iteritems():
                if isinstance(val, dict):
                    nested_obj = RecursiveDictAsObjectWrapper(**val)
                    setattr(obj, key, nested_obj)
                else:
                    setattr(obj, key, val)
        _update(self, kwargs)


def random_string(length, alphabet=None, lowercase=True, uppercase=True,
                  digits=True, special=True, extra=''):
    if alphabet is None:
        src = extra
        if lowercase:
            src += string.ascii_lowercase
        if uppercase:
            src += string.ascii_uppercase
        if digits:
            src += string.digits
        if special:
            src += '!@#$%^&*()_-+=?/><,.|":;`~'
    else:
        src = alphabet
    return ''.join(random.choice(src) for x in xrange(length))


def get_secret_key(key=None):
    if key is not None:
        return key
    else:
        from kaylee import kl
        if kl._wrapped is None:
            raise KayleeError('Cannot locate a valid secret key because '
                              'Kaylee proxy object has not beet set up.')
        key = kl.config.SECRET_KEY
        if key is None:
            raise KayleeError('SECRET_KEY configuration option is not '
                              'defined.')
        return key



def is_strong_subclass(C, B):
    """Return whether class C is a subclass (i.e., a derived class) of class B
    and C is not B.
    """
    return issubclass (C, B) and C is not B


@contextlib.contextmanager
def nostdout(stdout=True, stderr=True):
    savestderr = sys.stderr
    savestdout = sys.stdout
    class Devnull(object):
        def write(self, _):
            pass
    if stdout:
        sys.stdout = Devnull()
    if stderr:
        sys.stderr = Devnull()
    yield
    sys.stdout = savestdout
    sys.stderr = savestderr


def ensure_dir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

def setup_logging(loglevel=logging.INFO):
    log_format = '%(levelname)s[%(name)s]: %(message)s'
    logging.basicConfig(level=loglevel, format=log_format)
