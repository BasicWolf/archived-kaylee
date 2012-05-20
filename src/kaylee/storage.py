# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from .errors import KayleeError
from .objectid import NodeID
from .node import Node
from .py3compat import string_types, binary_type, string_type

class NodesStorage(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, node):
        """Add node to storage"""

    @abstractmethod
    def remove(self, node):
        """Remove node from storage"""

    @abstractmethod
    def __getitem__(self, node_id):
        """Return node with requested id"""

    @abstractmethod
    def __contains__(self, node):
        """Check if storage contains the node"""

    def _get_node_id(self, node):
        if isinstance(node, string_types):
            return NodeID(node_id = node)
        elif isinstance(node, NodeID):
            return node
        elif isinstance(node, Node):
            return node.id
        else:
            raise KayleeError('node must be an instance of {}, {}, {} or {} not'
                              ' {}'.format(binary_type.__name__, 
                                           string_type.__name__,
                                           NodeID.__name__,
                                           Node.__name__, type(node).__name__))
                    

class MemoryNodesStorage(NodesStorage):
    def __init__(self):
        self._d = {}

    def add(self, node):
        self._d[node.id] = node

    def remove(self, node):
        node_id = self._get_node_id(node)
        try:
            del self._d[node_id]
        except KeyError:
            pass

    def __getitem__(self, node_id):
        node_id = self._get_node_id(node_id)
        return self._d[node_id]

    def __contains__(self, node):
        node_id = self._get_node_id(node)
        return node_id in self._d


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
    def __setitem__(self, task_id, results):
        """Stores results associated with task_id to the storage.
        """

    @abstractmethod
    def __getitem__(self, task_id):
        """ """

    @abstractmethod
    def __delitem__(self, task_id):
        """Removes all results associated with task_id from the storage.
        """

    @abstractmethod
    def __contains__(self, task_id):
        """ """


class MemoryControllerResultsStorage(ControllerResultsStorage):
    def __init__(self):
        self._d = {}

    def add(self, node_id, task_id, result):
        """ """
        d = self._d.get(task_id, {})
        d[node_id] = result
        self._d[task_id] = d

    def remove(self, node_id, task_id):
        del self._d[task_id][node_id]

    def __getitem__(self, task_id):
        try:
            return self._d[task_id]
        except KeyError:
            return []

    def __setitem__(self, task_id, val):
        self._d[task_id] = val

    def __delitem__(self, task_id):
        del self._d[task_id]

    def __contains__(self, task_id):
        return task_id in self._d


class AppResultsStorage(object):
    """Applications results holder object. This class is an interface for
    objects which should hold the final results of an application. """
    __metaclass__ = ABCMeta

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
    def __next__(self):
        """ """

    def next(self):
        return self.__next__()


class MemoryAppResultsStorage(AppResultsStorage):
    def __init__(self):
        self._d = {}

    def __getitem__(self, task_id):
        """ """

    def __setitem__(self, task_id, result):
        """ """
        self._d[task_id] = result

    def __contains__(self, task_id):
        """ """

    def __iter__(self):
        """ """

    def __next__(self):
        """ """
