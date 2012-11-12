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
import random
import string
import cPickle as pickle
from datetime import timedelta
from abc import ABCMeta
from base64 import b64encode, b64decode
from hmac import new as hmac
from hashlib import sha1, sha256
from Crypto.Cipher import AES

from .errors import KayleeError


NO_AUTO_FILTERS = 0x0
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


def random_string(length, alphabet = None, lowercase = True, uppercase = True,
                  digits = True, extra = ''):
    if alphabet is not None:
        src = alphabet
    else:
        src = extra
        if lowercase:
            src += string.ascii_lowercase
        if uppercase:
            src += string.ascii_uppercase
        if digits:
            src += string.digits

    return ''.join(random.choice(src) for x in xrange(length))





#------------- Object attributes encryption --------------------#

def get_secret_key(key = None):
    if key is not None:
        return key
    else:
        from kaylee import kl
        if kl._wrapped is not None:
            key = kl.config.SECRET_KEY
            if key is None:
                raise KayleeError('SECRET_KEY configuration option is not'
                                  ' defined.')
            return key
        else:
            raise KayleeError('Cannot locate a valid secret key.')

def encrypt(data, secret_key=None):
    """Encrypt the data and return its base64 representation.

    :param data: Data to encrypt. The data is pickled prior to encryption.
    :param secret_key: A secret key to use.
    :type data: dict
    :type secret_key: str
    """
    secret_key = get_secret_key(secret_key)

    mac = hmac(secret_key, None, sha1)
    encryption_key = sha256(secret_key).digest()

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in xrange(16))
    encryptor = AES.new(encryption_key, AES.MODE_CBC, iv)

    b64_iv = b64encode(iv)
    result = [b64_iv]      # store initialization vector
    for key, val in data.iteritems():
        result.append(_encrypt_attr(key, val, encryptor))
        mac.update('|' + result[-1])

    return '{}?{}'.format(b64encode(mac.digest()), '&'.join(result))

def decrypt(s, secret_key=None):
    secret_key = get_secret_key(secret_key)
    base64_hash, data = s.split('?', 1)
    mac = hmac(secret_key, None, sha1)

    iv, data = data.split('&', 1)
    iv = b64decode(iv)

    decryption_key = sha256(secret_key).digest()
    decryptor = AES.new(decryption_key, AES.MODE_CBC, iv)

    res = {}
    for item in data.split('&'):
        mac.update('|' + item)
        attr, val = _decrypt_attr(item, decryptor)
        res[attr] = val

    if b64decode(base64_hash) == mac.digest():
        return res
    else:
        raise KayleeError('Encrypted data signature verification failed.')

def _encrypt_attr(attr, value, encryptor):
    BLOCK_SIZE = 32
    PADDING = ' '
    # one-liner to sufficiently pad the text to be encrypted
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

    val = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
    val = '{}={}'.format(attr, val)
    val = encryptor.encrypt(pad(val))
    val = b64encode(val)
    return val

def _decrypt_attr(data, decryptor):
    tdata = b64decode(data)
    tdata = decryptor.decrypt(tdata).rstrip(' ')
    attr, val = tdata.split('=', 1)
    val = pickle.loads(val)
    return attr, val
