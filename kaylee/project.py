# -*- coding: utf-8 -*-
"""
    kaylee.project
    ~~~~~~~~~~~~~~

    This module provides basic interfaces for Kaylee projects.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

import random
import cPickle as pickle
from base64 import b64encode, b64decode
from hmac import new as hmac
from hashlib import sha1, sha256
from abc import abstractmethod
from copy import copy
from functools import wraps
from copy import deepcopy

from Crypto.Cipher import AES

from .util import (AutoFilterABCMeta, BASE_FILTERS, CONFIG_FILTERS,
                   get_secret_key)
from .errors import KayleeError

DEPLETED = 0x2
COMPLETED = 0x4

def depleted_guard(f):
    """Catches :exc:`StopIteration`, sets ``project.depleted`` to
    ``True`` and re-throws the error.

    .. note:: This is a base filter applied to :meth:`Project.__next__`.
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except StopIteration as e:
            self.depleted = True
            raise e
    return wrapper

def ignore_null_result(f):
    """Ignores ``None`` data by **not** calling the wrapped method.

    .. note:: This is a base filter applied to :meth:`Project.normalize`
              and :meth:`Project.store_result`.
    """
    @wraps(f)
    def wrapper(self, task_id, data):
        if data is not None:
            return f(self, task_id, data)
        return None
    return wrapper


class Project(object):
    """Base class for Kaylee projects. Essentialy a Project is an
    iterator that yields Kaylee :class:`Tasks <Task>`.

    Every task has a unique ID and a project should be able
    to return the same task by the given id if required.

    Metaclass: :class:`AutoFilterABCMeta <kaylee.util.AutoFilterABCMeta>`.
    """

    __metaclass__ = AutoFilterABCMeta
    auto_filter = BASE_FILTERS | CONFIG_FILTERS
    auto_filters = {
        '__next__' : [depleted_guard, ],
        'normalize' : [ignore_null_result, ],
        'store_result' : [ignore_null_result, ],
       }


    def __init__(self, storage = None, *args, **kwargs):
        #: A dictionary with configuration
        #: details used by every client-side node. By-default it
        #: contains a URL of the script with project's client-side
        #: logic. If the project is loaded via a configuration object
        #: ``client_config`` is extended by ``project.config`` section's
        #: value (see :ref:`loading`).
        self.client_config = {
            'script' : kwargs['script'],
            }
        self.storage = storage
        self._state = 0

    def next(self):
        """Same as :meth:`__next__` ."""
        return self.__next__()

    @abstractmethod
    def __next__(self):
        """
        Returns the next task. The :exc:`StopIteration` exception thrown
        by ``__next__()`` indicates that there will be no more
        new tasks from the project, but the bound controller can still
        refer to old tasks via ``project[task_id]``. After :exc:`StopIteration`
        has been thrown, :attr:`Project.depleted` *must* be set (by the project
        or via auto filter) to ``True``.
        If the controller does not intercept or re-throws :exc:`StopIteration`,
        Kaylee catches and interprets it as *"no need to involve the bound node
        in any further calculations for the application"*.

        :throws: StopIteration
        :returns: an instance of :class:`Task`
        """

    @abstractmethod
    def __getitem__(self, task_id):
        """Returns task with the required id."""

    def store_result(self, task_id, data):
        """Stores the results to the permanent storage.

        :param task_id: Task ID.
        :param data: Task results.
        :type data: dict or list (parsed JSON)
        """
        self.storage.add(task_id, data)

    @property
    def depleted(self):
        """Indicates if current project instance has run out of new tasks
        (see :meth:`Project.__next__`).
        """
        return self._state & DEPLETED

    @depleted.setter
    def depleted(self, val):
        if val:
            self._state |= DEPLETED
        else:
            self._state &= ~DEPLETED

    @property
    def completed(self):
        """Indicates whether the project was completed."""
        return self._state & COMPLETED

    @completed.setter
    def completed(self, val):
        if val:
            self._state |= COMPLETED
        else:
            self._state &= ~COMPLETED

    def normalize(self, task_id, data):
        """Normalizes and validates a solution.

        :param task_id: the ID of the task.
        :param data: the solution to be validated and/or normalized.
        :throws ValueError: if the data is invalid.
        :return: normalized data.
        """
        return data

class TaskMeta(type):
    """
    The metaclass for :class:`Task`. Adds **serializable**
    attribute logic to the class. This attribute is a list
    which contains the names of the Task's attributes that
    are stored into a dictionary which is then returned
    by the serialize() method. This dictionary can be used to
    e.g. export the object to JSON.
    """
    def __new__(mcs, classname, bases, class_dict):
        serializable = []
        if 'serializable' in class_dict:
            serializable = class_dict['serializable']

        for base in bases:
            if hasattr(base, 'serializable'):
                # extend from left side of the list
                serializable[:-len(serializable)] = base.serializable
        class_dict['serializable'] = serializable
        return type.__new__(mcs, classname, bases, class_dict)


class Task(object):
    """
    Base class for Kaylee projects' tasks. This class is meant to be
    inherited in users' projects if additional attributes-to-be-serialized
    are required. When serialized, ``Task.id`` is converted to string,
    whereas other attributes' values are stored unmodified.
    For example::

        class MyTask(Task):
            serializable = ['speed']

            def __init__(self, task_id, speed):
                super(MyTask, self).__init__(task_id)
                self.speed = speed

        task = MyTask('001', 60)
        task.serialize()
        # >>> { 'id' : '001', 'speed' : 60 }


    :param task_id: Unique task id.
    :type task_id: string
    """
    __metaclass__ = TaskMeta
    serializable = ['id']

    def __init__(self, task_id):
        self.id = str(task_id)

    def serialize(self, attributes = None, secret_key = None):
        """
        Serializes object attributes to dict.

        :param attributes: A custom list of attributes which overrides
                           ``self.serializable``.
        """
        result = {}
        if attributes is None:
            attributes = self.serializable

        res = { attr : getattr(self, attr) for attr in attributes
                if not attr.startswith('#') }

        # process session attributes, if any
        sess_attributes = [attr[1:] for attr in attributes if attr.startswith('#')]
        if len(sess_attributes) > 0:
            res['__kaylee_task_session__'] = self.encrypt(sess_attributes,
                                                          secret_key)
        return res

    def encrypt(self, attributes, secret_key = None):
        secret_key = get_secret_key(secret_key)

        mac = hmac(secret_key, None, sha1)
        encryption_key = sha256(secret_key).digest()

        iv = ''.join(chr(random.randint(0, 0xFF)) for i in xrange(16))
        encryptor = AES.new(encryption_key, AES.MODE_CBC, iv)

        b64_iv = b64encode(iv)
        result = [b64_iv]      # store initialization vector
        for attr in sorted(attributes):
            value = getattr(self, attr)
            result.append(Task._encrypt_attr(attr, value, encryptor))
            mac.update('|' + result[-1])

        return '{}?{}'.format(b64encode(mac.digest()), '&'.join(result))

    @staticmethod
    def deserialize(d, secret_key = None):
        result = {}

        if isinstance(d, dict):
            s = d['__kaylee_task_session__']
            result = deepcopy(d)
            del result['__kaylee_task_session__']
        else:
            s = d

        secret_key = get_secret_key(secret_key)
        base64_hash, data = s.split('?', 1)
        mac = hmac(secret_key, None, sha1)

        iv, data = data.split('&', 1)
        iv = b64decode(iv)

        decryption_key = sha256(secret_key).digest()
        decryptor = AES.new(decryption_key, AES.MODE_CBC, iv)

        for item in data.split('&'):
            mac.update('|' + item)
            attr, val = Task._decrypt_attr(item, decryptor)
            result[attr] = val

        if b64decode(base64_hash) == mac.digest():
            return result
        else:
            raise KayleeError('Session attribute signature verification failed.')

    @staticmethod
    def _encrypt_attr(attr, val, encryptor):
        BLOCK_SIZE = 32
        PADDING = ' '
        # one-liner to sufficiently pad the text to be encrypted
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

        val = pickle.dumps(val, pickle.HIGHEST_PROTOCOL)
        val = '{}={}'.format(attr, val)
        val = encryptor.encrypt(pad(val))
        val = b64encode(val)
        return val

    @staticmethod
    def _decrypt_attr(data, decryptor):
        data = b64decode(data)
        data = decryptor.decrypt(data).rstrip(' ')
        attr, val = data.split('=', 1)
        val = pickle.loads(val)
        return attr, val


    def __str__(self):
        return 'Task: ' + '; '.join('{0}: {1}'.format(attr, getattr(self, attr))
                                    for attr in self.serializable )
