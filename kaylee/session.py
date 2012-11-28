import cPickle as pickle
from base64 import b64encode, b64decode
from hmac import new as hmac
from hashlib import sha1, sha256
from Crypto.Cipher import AES

from .util import get_secret_key


class SessionDataManager(object):
    def store(self, node, task_data):
        pass

    def restore(self, node, result_data):
        pass


class JSONSessionDataManager(SessionDataManager):

    def store(self, node, task_data):
        

    @classmethod
    def _encrypt(cls, data, secret_key):
        """Encrypt the data and return its base64 representation.

        :param data: Data to encrypt. The data is pickled prior to encryption.
        :param secret_key: A secret key to use.
        :type data: dict
        :type secret_key: str
        """
        mac = hmac(secret_key, None, sha1)
        encryption_key = sha256(secret_key).digest()

        iv = ''.join(chr(random.randint(0, 0xFF)) for i in xrange(16))
        encryptor = AES.new(encryption_key, AES.MODE_CBC, iv)

        b64_iv = b64encode(iv)
        result = [b64_iv]      # store initialization vector
        for key, val in data.iteritems():
            result.append(cls._encrypt_attr(key, val, encryptor))
            mac.update('|' + result[-1])

        return '{}?{}'.format(b64encode(mac.digest()), '&'.join(result))

    @classmethod
    def _decrypt(cls, s, secret_key):
        base64_hash, data = s.split('?', 1)
        mac = hmac(secret_key, None, sha1)

        iv, data = data.split('&', 1)
        iv = b64decode(iv)

        decryption_key = sha256(secret_key).digest()
        decryptor = AES.new(decryption_key, AES.MODE_CBC, iv)

        res = {}
        for item in data.split('&'):
            mac.update('|' + item)
            attr, val = cls._decrypt_attr(item, decryptor)
            res[attr] = val

        if b64decode(base64_hash) == mac.digest():
            return res
        else:
            raise KayleeError('Encrypted data signature verification failed.')

    @classmethod
    def _encrypt_attr(cls, attr, value, encryptor):
        BLOCK_SIZE = 32
        PADDING = ' '
        # one-liner to sufficiently pad the text to be encrypted
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

        val = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        val = '{}={}'.format(attr, val)
        val = encryptor.encrypt(pad(val))
        val = b64encode(val)
        return val

    @classmethod
    def _decrypt_attr(cls, data, decryptor):
        tdata = b64decode(data)
        tdata = decryptor.decrypt(tdata).rstrip(' ')
        attr, val = tdata.split('=', 1)
        val = pickle.loads(val)
        return attr, val
