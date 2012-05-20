# Based on the code from pymongo package.
# The preserved copyright notice:
# # Copyright 2009-2012 10gen, Inc.
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# # http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

import binascii
import struct
import threading
import time
import datetime
import zlib
from .py3compat import b, string_types, binary_type, string_type, bytes_from_hex
from .errors import InvalidNodeIDError
from .tz_util import utc

EMPTY = b("")


def _crc32(data):
    return zlib.crc32(b(data)) & 0xffffffff


class NodeID(object):
    __slots__ = ('_id')
    _inc = 0
    _inc_lock = threading.Lock()

    def __init__(self, remote_host = None, node_id = None):
        if node_id is None and not isinstance(remote_host, string_types):
            raise TypeError('remote_host must be an instance of ({}, {}), not {}'
                            .format(binary_type.__name__, string_type.__name__,
                                    type(remote_host)))
        if node_id is None:
            self._generate(remote_host)
        else:
            self._parse(node_id)

    def _generate(self, remote_host):
        """Generate a new value for this NodeID.
        """
        nid = EMPTY
        # 4 bytes current time
        nid += struct.pack('>i', int(time.time()))
        # 4 bytes host
        nid += struct.pack('>I', _crc32(remote_host))
        # 2 bytes inc
        with NodeID._inc_lock:
            NodeID._inc = (NodeID._inc + 1) % 0xFFFF
            nid += struct.pack(">i", NodeID._inc)[2:4]
        # 10 bytes total
        self._id = nid

    def _parse(self, nid):
        """Validate and use the given id for this NodeID.

        Raises TypeError if id is not an instance of (:class:`basestring`
        (:class:`str` or :class:`bytes` in python 3), NodeID) and InvalidId if
        it is not a valid NodeID.

        :Parameters:
          - `nid`: a valid NodeID
        """
        if isinstance(nid, NodeID):
            self._id = nid._id
        elif isinstance(nid, string_types):
            if len(nid) == 10:
                if isinstance(nid, binary_type):
                    self._id = nid
                else:
                    raise InvalidNodeIDError(nid)
            elif len(nid) == 20:
                try:
                    self._id = bytes_from_hex(nid)
                except (TypeError, ValueError):
                    raise InvalidNodeIDError(nid)
            else:
                raise InvalidNodeIDError(nid)
        else:
            raise TypeError('id must be an instance of ({}, {}, NodeID), not {}'
                            .format(binary_type.__name__, string_type.__name__,
                                    type(nid)))

    @property
    def binary(self):
        """10-byte binary representation of this NodeID.
        """
        return self._id

    @property
    def generation_time(self):
        """A :class:`datetime.datetime` instance representing the time of
        generation for this :class:`NodeID`.

        The :class:`datetime.datetime` is timezone aware, and
        represents the generation time in UTC. It is precise to the
        second.
        """
        t = struct.unpack(">i", self._id[0:4])[0]
        return datetime.datetime.fromtimestamp(t, utc)

    def __str__(self):
        return binascii.hexlify(self._id).decode()

    def __repr__(self):
        return "NodeID('{}')".format(str(self))

    def __eq__(self, other):
        if isinstance(other, NodeID):
            return self._id == other._id
        return NotImplemented

    def __ne__(self,other):
        if isinstance(other, NodeID):
            return self._id != other._id
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, NodeID):
            return self._id < other._id
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, NodeID):
            return self._id <= other._id
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, NodeID):
            return self._id > other._id
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, NodeID):
            return self._id >= other._id
        return NotImplemented

    def __hash__(self):
        """Get a hash value for this :class:`NodeID`.
        """
        return hash(self._id)
