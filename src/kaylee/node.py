# -*- coding: utf-8 -*-
# NodeID class is based on the code from pymongo package.
# See NOTICE for more details
"""
    kaylee.node
    ~~~~~~~~~~~

    Implements Kaylee server-side node classes.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime
import time
import binascii
import struct
import threading
import zlib
from .errors import InvalidNodeIDError
from .tz_util import utc


class Node(object):
    """
    A Node object contains information about a node which was registered
    by :class:`Kaylee`. Its id field is an instance :class:`NodeID`
    which allows to track when the node was registered. Other public
    fields are:

    * subscription_timestamp - a :class:`datetime.datetime` instance which
      tracks the time when a node has subscribed to an application.
    * task_timestamp a :class:`datetime.datetime` instance which
      tracks the time when a node has received its last to-compute task.
    * controller a reference or an id of a application's
      :class:`Controller`  object
    """
    __slots__ = ('id', '_task_id', 'subscription_timestamp', 'task_timestamp',
                 'controller')

    def __init__(self, node_id):
        if not isinstance(node_id, NodeID):
            raise TypeError('node_id must be an instance of {}, not {}'
                            .format(NodeID.__name__,
                                    type(node_id).__name__ )
                            )
        self.id = node_id
        self.reset()

    def reset(self):
        self._task_id = None
        self.subscription_timestamp = None
        self.task_timestamp = None
        self.controller = None

    def get_task(self):
        return self.controller.get_task(self)

    def accept_result(self, data):
        self.controller.accept_result(self, data)

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, val):
        self._task_id = val
        self.task_timestamp = datetime.now()

    def __hash__(self):
        return hash(self.id)


class NodeID(object):
    __slots__ = ('_id')
    _inc = 0
    _inc_lock = threading.Lock()

    def __init__(self, node_id = None, remote_host = '127.0.0.1'):
        if node_id is None and not isinstance(remote_host, basestring):
            raise TypeError('remote_host must be an instance of {}, not {}'
                            .format(basestring.__name__,
                                    type(remote_host).__name__ )
                            )
        if node_id is None:
            self._generate(remote_host)
        else:
            self._parse(node_id)

    @staticmethod
    def for_host(host):
        return NodeID(remote_host = host)

    def _generate(self, remote_host):
        """Generate a new value for this NodeID."""
        nid = b''
        # 4 bytes current time
        nid += struct.pack('>i', int(time.time()))
        # 4 bytes host
        nid += struct.pack('>I', self._crc32(remote_host))
        # 2 bytes inc
        with NodeID._inc_lock:
            nid += struct.pack(">i", NodeID._inc)[2:4]
            NodeID._inc = (NodeID._inc + 1) % 0xFFFF
        # 10 bytes total
        self._id = nid

    def _parse(self, nid):
        if isinstance(nid, NodeID):
            self._id = nid._id
        elif isinstance(nid, basestring):
            if len(nid) == 10:
                if isinstance(nid, str):
                    self._id = nid
                else:
                    raise InvalidNodeIDError(nid)
            elif len(nid) == 20:
                try:
                    self._id = nid.decode('hex')
                except (TypeError, ValueError):
                    raise InvalidNodeIDError(nid)
            else:
                raise InvalidNodeIDError(nid)
        else:
            raise TypeError('id must be an instance of {}, {} or {}, not {}'
                            .format(str.__name__,
                                    unicode.__name__,
                                    self.__class__.__name__,
                                    type(nid).__name__))

    def _crc32(self, data):
        return zlib.crc32(data) & 0xffffffff

    @property
    def binary(self):
        """10-byte binary representation of this NodeID."""
        return self._id

    @property
    def generation_time(self):
        """
        A :class:`datetime.datetime` instance representing the time of
        generation for this :class:`NodeID`.

        The :class:`datetime.datetime` is timezone aware, and
        represents the generation time in UTC. It is precise to the
        second.
        """
        t = struct.unpack(">i", self._id[0:4])[0]
        return datetime.fromtimestamp(t, utc)

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
