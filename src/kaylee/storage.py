# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from datetime import datetime

from .errors import KayleeError
from .node import Node, NodeID
from .util import parse_timedelta


class NodesStorage(object):
    """
    The interface for registered nodes storage. A NodesStorage is a place
    where Kaylee keeps information about active Nodes. It can be as simple
    as Python collection or as complex as MongoDB or memcached - that is
    for the user to choose.
    The implementation of NodesStorage should accept and return
    :class:`Node` objects. (TODO: see Mem...)
    """
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def add(self, node):
        """Adds node to storage."""

    @abstractmethod
    def clean(self, node):
        """Removes the obsolete nodes from the storage."""

    @abstractmethod
    def __delitem__(self, node):
        """Removes the node from the storage."""

    @abstractmethod
    def __getitem__(self, node_id):
        """Returns a node with the requested id."""

    @abstractmethod
    def __contains__(self, node):
        """Checks if the storage contains the node."""


class ControllerResultsStorage(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, node_id, task_id, result):
        """Stores results from particular node associated with task_id to the
        storage.
        """

    @abstractmethod
    def remove(self, node_id, task_id):
        """Removes result recieved from particular node associated with task_id
        from the storage.
        """

    @abstractmethod
    def clear(self):
        """ """

    @abstractmethod
    def __setitem__(self, task_id, results):
        """Stores results associated with task_id to the storage."""

    @abstractmethod
    def __getitem__(self, task_id):
        """ """

    @abstractmethod
    def __delitem__(self, task_id):
        """Removes all results associated with task_id from the storage."""

    @abstractmethod
    def __contains__(self, task_id):
        """ """


class ProjectResultsStorage(object):
    """Applications results holder object. This class is an interface for
    objects which should hold the final results of an application. """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __len__(self):
        """ """

    @abstractmethod
    def __getitem__(self, task_id):
        """ """

    @abstractmethod
    def __setitem__(self, task_id, result):
        """ """

    @abstractmethod
    def __contains__(self, task_id):
        """ """

    @abstractmethod
    def __iter__(self):
        """ """

    @abstractmethod
    def keys(self):
        """ """

    @abstractmethod
    def values(self):
        """ """