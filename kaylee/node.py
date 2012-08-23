# -*- coding: utf-8 -*-
"""
    kaylee.node
    ~~~~~~~~~~~

    Implements Kaylee server-side node classes.
    The NodeID class is partially based on the code from pymongo package.
    See NOTICE for more details

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

import time
import binascii
import struct
import threading
import hashlib
from datetime import datetime
from abc import ABCMeta, abstractmethod

from .errors import InvalidNodeIDError, NodeUnsubscribedError
from .util import parse_timedelta

#: The hex string formatted NodeID regular expression pattern which
#: can be used in e.g. web frameworks' URL dispatchers.
node_id_pattern = r'[\da-fA-F]{20}'


class Node(object):
    """
    A Node object contains information about a node which was registered
    by :class:`Kaylee`.

    :param node_id: an instance of :class:`NodeID` or a string parsable by
                    :class:`NodeID`
    """
    __slots__ = ('id', '_task_id', 'subscription_timestamp', 'task_timestamp',
                 'controller')

    def __init__(self, node_id):
        if not isinstance(node_id, NodeID):
            raise TypeError('node_id must be an instance of {}, not {}'
                            .format(NodeID.__name__,  type(node_id).__name__ ))
        #: An instance of :class:`NodeID`
        self.id = node_id

        #: A :class:`datetime.datetime` instance which tracks the time
        #: when a node has subscribed to an application.
        self.subscription_timestamp = None

        #: A :class:`datetime.datetime` instance which tracks the time
        #: of a node receiving its last to-compute task.
        self.task_timestamp = None

        #: Application which communicates with the node.
        #: It is an instance of :class:`Controller`.
        self.controller = None

        self._task_id = None

    def unsubscribe(self):
        self.subscription_timestamp = None
        self.task_timestamp = None
        self.controller = None
        self._task_id = None

    def get_task(self):
        if self.controller is None:
            raise NodeUnsubscribedError(self)
        return self.controller.get_task(self)

    def accept_result(self, data):
        if self.controller is None:
            raise NodeUnsubscribedError(self)
        self.controller.accept_result(self, data)

    @property
    def task_id(self):
        """The ID of the task being solved by the node."""
        return self._task_id

    @task_id.setter
    def task_id(self, val):
        self._task_id = val
        self.task_timestamp = datetime.now()

    def __hash__(self):
        return hash(self.id)


class NodeID(object):
    """
    NodeID is a 10-bytes long ID generated from current UNIX time,
    remote host identifier and internal incremental counter.
    The format is::

    [UNIX time (4)][counter (2)][remote host identifier hash (4)]

    Usually a new NodeID object is generated as follows::

        n = NodeID.for_host('192.168.10.20')

    The NodeID objects can be effectively compared in order to find out,
    which one was created earlier, e.g.::

        NodeID() < NodeID()
        # >>> True

    Is always ``True``, no matter what the remote host is.
    Another useful conversion is::

        n1 = NodeID()
        n2 = NodeID( str(NodeID) )
        n1 == n2
        # >>> True

    The NodeID object can be also effectively used as a key in collections::

        n1 = NodeID()
        d = { n1: 'some_val' }
        n2 = NodeID( str(NodeID) )
        n2 in d
        # >>> True

    :param node_id: A valid node id. The string representation of the
                    NodeID object is either binary 10-bytes long string
                    or 20-characters long hex string. If ``node_id``
                    is ``None``, then a new NodeID is generated.
    :param remote_host: Remote host IP address or other identifier.
    :type node_id: string, NodeID object or ``None``
    :type remote_host: string
    :throws: TypeError
    """
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
        """Constructs a new NodeID object from remote host identifier.

        :param host: remote host identifier
        :type host: string
        :returns: NodeID object
        """
        return NodeID(remote_host = host)

    @staticmethod
    def from_object(node):
        """Extracts or constructs NodeID from the given object.

        :param node: a valid NodeID or previously initialized Kaylee Node
                     object.
        :type node: string, NodeID or :class:`Node`
        :throws: TypeError
        :returns: NodeID object
        """
        if isinstance(node, basestring):
            return NodeID(node_id = node)
        elif isinstance(node, NodeID):
            return node
        elif isinstance(node, Node):
            return node.id
        else:
            raise TypeError('node must be an instance of {}, {}, or {} not'
                            ' {}'.format(basestring.__name__,
                                         NodeID.__name__,
                                         Node.__name__,
                                         type(node).__name__))

    def _generate(self, remote_host):
        """Generates a new value for this NodeID."""
        nid = b''
        # 4 bytes current time
        nid += struct.pack('>i', int(time.time()))
        # 2 bytes inc
        with NodeID._inc_lock:
            nid += struct.pack(">i", NodeID._inc)[2:4]
            NodeID._inc = (NodeID._inc + 1) % 0xFFFF
        # 4 bytes host
        host_hash = hashlib.md5()
        host_hash.update(remote_host)
        nid += host_hash.digest()[0:4]
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

    @property
    def binary(self):
        """10-byte binary representation of the NodeID.

        :returns: string
        """
        return self._id

    @property
    def timestamp(self):
        """A timezone-aware :class:`datetime.datetime` instance representing
        the current NodeID's generation time. It is precise to a second.
        """
        t = struct.unpack(">i", self._id[0:4])[0]
        return datetime.fromtimestamp(t)

    def __str__(self):
        """Hex representation of the  NodeID"""
        return binascii.hexlify(self._id).decode()

    def __repr__(self):
        return "NodeID('{}')".format(str(self))

    def __eq__(self, other):
        other = NodeID.from_object(other)
        return self._id == other._id

    def __ne__(self, other):
        other = NodeID.from_object(other)
        return self._id != other._id

    def __lt__(self, other):
        other = NodeID.from_object(other)
        return self._id < other._id

    def __le__(self, other):
        other = NodeID.from_object(other)
        return self._id <= other._id

    def __gt__(self, other):
        other = NodeID.from_object(other)
        return self._id > other._id

    def __ge__(self, other):
        other = NodeID.from_object(other)
        return self._id >= other._id

    def __hash__(self):
        """NodeID's hash"""
        return hash(self._id)


class NodesRegistry(object):
    """
    The interface for registered nodes storage. A NodesRegistry is a place
    where Kaylee keeps information about active  Nodes. It can be as simple
    as Python collection or as complex as MongoDB or memcached - that is
    for the user to choose.

    :param timeout: Nodes timeout. Used by :meth:`clean` to determine if a
                    node is obsolete.
                    Format: ``1d 12h 10m 5s``, e.g. ``"12h"``; ``"1d 10m"``
                    etc.
    :type timeout: str
    """
    __metaclass__ = ABCMeta

    def __init__(self, timeout = '30m', *args, **kwargs):
        #: Nodes timeout. Parsed from constructors ``timeout`` argument.
        #: Type: :class:`datetime.timedelta`.
        self.timeout = parse_timedelta(timeout)

    @abstractmethod
    def add(self, node):
        """Adds node to the storage."""

    @abstractmethod
    def clean(self):
        """Removes the obsolete nodes from the storage."""

    @abstractmethod
    def __len__(self):
        """Returns the amount of nodes in the storage."""

    @abstractmethod
    def __delitem__(self, node):
        """Removes the node from the storage.

        :param node: an instance of :class:`Node` or a valid node id.
        """

    @abstractmethod
    def __getitem__(self, node_id):
        """Returns a node with the requested id."""

    @abstractmethod
    def __contains__(self, node):
        """Checks if the storage contains the node.

        :param node: an instance of :class:`Node` or a valid node id.
        """
