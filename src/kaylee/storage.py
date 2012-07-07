# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from datetime import datetime


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
    def __len__(self):
        """Returns the amount of nodes in the storage."""

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
    """The interface for applications' temporal results storage.
    Consider a situation, when a controller gives the same task to
    several nodes and the end result would be the mean value of
    the returned results. To store these temporal results unless
    all Nodes finish computation, an instance of
    ControllerResultsStorage should be used.

    Note that this storage is purely controller-specific. A particular
    controller may not use a temporal storage at all.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, node_id, task_id, result):
        """Stores the results associated with task computed by a node."""

    @abstractmethod
    def remove(self, node_id, task_id):
        """Removes the result associated with task computed by given node
        from the storage."""

    @abstractmethod
    def clear(self):
        """Removes all results from the storage."""

    @abstractmethod
    def __len__(self):
        """Returns the total amount of results in the storage."""

    @abstractmethod
    def __setitem__(self, task_id, results):
        """Stores the results associated with task."""

    @abstractmethod
    def __getitem__(self, task_id):
        """Returns the results associated with task.

        :rtype:  { node_id : result, ...} dict
        """

    @abstractmethod
    def __delitem__(self, task_id):
        """Removes all results associated with task."""

    @abstractmethod
    def __contains__(self, task_id):
        """Checks if there are any results associated with task."""


class ProjectResultsStorage(object):
    """The interface for applications' permanent results storage.
    The storage can be a file, a database, a Python object in memory etc.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __len__(self):
        """Returns the total amount of results in the storage."""

    @abstractmethod
    def __getitem__(self, task_id):
        """Returns the result associated with task."""

    @abstractmethod
    def __setitem__(self, task_id, result):
        """Stores the results of the given task."""

    @abstractmethod
    def __delitem__(self, task_id):
        """Removes the results of the given task."""

    @abstractmethod
    def __contains__(self, task_id):
        """Checks if results of the task are in the storage."""

    @abstractmethod
    def __iter__(self):
        """Returns the iterator object of the storage."""

    @abstractmethod
    def keys(self):
        """Returns an iterator object of the storage's keys."""

    @abstractmethod
    def values(self):
        """Returns an iterator object of the storage's values."""
