# -*- coding: utf-8 -*-

from .objectid import NodeID
from .node import Node
from .py3compat import string_types

class NodesStorage(object):
    def add(self, node):
        """Add node to storage"""

    def remove(self, node):
        """Remove node from storage"""

    def __getitem__(self, nid):
        """Return node with requested id"""

    def __contains__(self, node):
        """Check if storage contains the node"""

    def _get_nid(self, node):
        if isinstance(node, string_types):
            return NodeID(nid = node)
        elif isinstance(node, NodeID):
            return node
        elif isinstance(node, Node):
            return node.id


class MemoryNodesStorage(NodesStorage):
    def __init__(self):
        self._dict = {}

    def add(self, node):
        self._dict[node.id] = node

    def remove(self, node):
        nid = self._get_nid(node)
        del self._dict[nid]

    def __getitem__(self, nid):
        return self._dict[nid]

    def __contains__(self, node):
        nid = self._get_nid(node)
        return self._dict.has_key(nid)
