# -*- coding: utf-8 -*-
"""
    kaylee.session
    ~~~~~~~~~~~~~~

    This module provides base interface for managing session data
    and contains its basic implementations.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""
#Pylint false alarm of missing hashlib functions
#pylint: disable-msg=E0611

import random
import cPickle as pickle
from base64 import b64encode, b64decode
from hmac import new as hmac
from hashlib import sha1, sha256
from Crypto.Cipher import AES
from abc import ABCMeta, abstractmethod

from .util import get_secret_key
from .errors import KayleeError

SESSION_DATA_ATTRIBUTE = '__kl_sd__'

class SessionDataManager(object):
    """The abstract base class representing Session data manager
    interface.

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def store(self, node, task):
        """Stores the session variables found in task and then  removes
        these variables from the task, e.g. the ``#s1`` and ``#s2``
        session variables should be removed in the following task::

          task = {
              'id' : 'i1',
              '#s1' : 10,
              '#s2' : [1, 2, 3]
          }

          manager.store(task)

          # task -> { 'id' : 'i1' }.


        :param node: the node to which the current task will be sent.
        :param task: task with or without session data. The task is accessed
                     by reference and is modified in-place.
        :type node: :class:`NodeID`
        :type task: dict
        """

    @abstractmethod
    def restore(self, node, result):
        """Restores the session variables and attaches them to the result.

        :param node: the node from which the result was received.
        :param result: the result to which the session data is attached. The
                       result is accessed by reference and is modified
                       in-place.
        :type node: :class:`NodeID`
        :type result: dict
        """

    @staticmethod
    def get_session_data(task):
        """Returns a dict with session variables found in task."""
        return { key : task[key] for key in task
                 if key.startswith('#') }

    @staticmethod
    def remove_session_data_from_task(session_data_keys, task):
        for key in session_data_keys:
            del task[key]


class PhonySessionDataManager(SessionDataManager):
    """The default session data manager which throws :class:`KayleeError`
    if any session variables are encountered in an outgoing task."""
    def store(self, node, task):
        session_data = self.get_session_data(task)
        if session_data == {}:
            return
        else:
            raise KayleeError('Cannot store session data in a '
                              'phony data manager')

    def restore(self, node, result):
        pass

KL_LOADER_DEFAULT_SESSION_DATA_MANAGER = PhonySessionDataManager


class NodeSessionDataManager(SessionDataManager):
    """A session data manager, which keeps the data in
    :attr:`Node.session_data`."""
    def store(self, node, task):
        session_data = self.get_session_data(task)
        if session_data == {}:
            return

        node.session_data = pickle.dumps(session_data, pickle.HIGHEST_PROTOCOL)
        self.remove_session_data_from_task(session_data.iterkeys(), task)

    def restore(self, node, result):
        if node.session_data is None:
            return
        session_data = pickle.loads(node.session_data)
        node.session_data = None
        result.update(session_data)


class JSONSessionDataManager(SessionDataManager):
    """Stores encrypted session variables in task and restores them
    from the results. For example, the following task data::

      task = {
          'id' : 'i1',
          '#s1' : 10,
          '#s2' : [1, 2, 3]
      }

    Encrypted via the "abc" secret key turns into::

      task = {
          id : 'i1',
          '__kl_sd__' : 'yn/fCyEcW8AFrPps7XoxunC...' # 143 chars in total
      }

    The Kaylee client-side engine automatically attaches the ``'__kl_sd__``
    data to the JSON result sent to the server, so that the session data
    could be decrypted and restored, e.g.::

      {
          'speed' : 20,
          '#s1' : 10,
          '#s2' : [1, 2, 3]
      }

    :param secret_key: An override of the global :config:`SECRET_KEY`
                       configuration parameter.
    """
    def __init__(self, secret_key=None):
        #pylint: disable-msg=W0231
        #W0231: __init__ method from base class 'SessionDataManager'
        #       is not called.
        self._secret_key = secret_key
        self.SESSION_DATA_ATTRIBUTE = SESSION_DATA_ATTRIBUTE

    def store(self, node, task):
        session_data = self.get_session_data(task)
        if session_data == {}:
            return

        task[self.SESSION_DATA_ATTRIBUTE] =  _encrypt(session_data,
                                                      self.secret_key)
        self.remove_session_data_from_task(session_data.iterkeys(), task)

    def restore(self, node, result):
        if self.SESSION_DATA_ATTRIBUTE not in result:
            return
        sd = _decrypt(result[self.SESSION_DATA_ATTRIBUTE], self.secret_key)
        del result[self.SESSION_DATA_ATTRIBUTE]
        result.update(sd)

    @property
    def secret_key(self):
        if self._secret_key is None:
            self._secret_key = get_secret_key()
        return self._secret_key


def _encrypt(data, secret_key):
    """Encrypt the data and return its base64 representation.

    :param data: Data to encrypt. The data is pickled prior to encryption.
    :param secret_key: A secret key to use.
    :type data: any pickable Python object
    :type secret_key: str
    """
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


def _decrypt(s, secret_key):
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
