import random
import cPickle as pickle
from base64 import b64encode, b64decode
from hmac import new as hmac
from hashlib import sha1, sha256
from Crypto.Cipher import AES

from .util import get_secret_key
from .errors import KayleeError

SESSION_DATA_ATTRIBUTE = '__kl_sd__'

class SessionDataManager(object):
    def store(self, node, task):
        """TODOC"""
        pass

    def restore(self, node, result):
        """TODOC"""
        pass

    def _get_session_data(self, task):
        """TODOC"""
        return { key : task[key] for key in task
                 if key.startswith('#') }

    def _remove_session_data_from_task(self, session_data_keys, task):
        for key in session_data_keys:
            del task[key]


class NodeSessionDataManager(SessionDataManager):
    def store(self, node, task):
        sdata = self._get_session_data(task)
        node.session_data = pickle.dumps(sdata, pickle.HIGHEST_PROTOCOL)
        self._remove_session_data_from_task(sdata.iterkeys(), task)

    def restore(self, node, result):
        sdata = pickle.loads(node.session_data)
        result.update(sdata)


class JSONSessionDataManager(SessionDataManager):
    """Stores encrypted session data in task data and restores the session
    data from the results. For example, the following task data::

      task = {
          'id' : 'i1',
          '#s1' : 10,
          '#s2' : [1, 2, 3]
      }

    Is encrypted via 'abc' secret key, turns into::

      task = {
          id : 'i1',
          '__kl_sd__' : 'yn/fCyEcW8AFrPps7XoxunC...' # 143 chars in total
      }

    The Kaylee client-side engine automatically attaches the ``'__kl_sd__``
    data to the result, so that the session data is decrypted and attached
    back to the result, e.g.::

      {
          'speed' : 20,
          '#s1' : 10,
          '#s2' : [1, 2, 3]
      }
    """

    def __init__(self, *args, **kwargs):
        self._secret_key = kwargs.get('secret_key', None)
        self.SESSION_DATA_ATTRIBUTE = SESSION_DATA_ATTRIBUTE

    def store(self, node, task):
        session_data = self._get_session_data(task)
        task[self.SESSION_DATA_ATTRIBUTE] =  _encrypt(session_data,
                                                      self.secret_key)
        for key in session_data:
            del task[key]
        return task

    def restore(self, node, result):
        sd = _decrypt(result[self.SESSION_DATA_ATTRIBUTE], self.secret_key)
        del result[self.SESSION_DATA_ATTRIBUTE]
        result.update(sd)
        return result

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
