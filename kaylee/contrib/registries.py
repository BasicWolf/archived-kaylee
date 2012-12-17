# -*- coding: utf-8 -*-
from datetime import datetime
from kaylee.node import NodesRegistry, NodeID


class MemoryNodesRegistry(NodesRegistry):
    def __init__(self, *args, **kwargs):
        super(MemoryNodesRegistry, self).__init__(*args, **kwargs)
        self._d = {}

    def add(self, node):
        self._d[node.id] = node

    def update(self, node):
        # a very naive and simple update
        if node.id in self._d and node.dirty:
            self._d[node.id] = node
        else:
            raise KeyError('Cannot update node in registry: '
                           'node {} was not found'.format(node))

    def clean(self):
        nodes_to_clean = (node for node in self._d.iteritems()
                          if datetime.now() - node.id.timestamp > self.timeout)
        for node in nodes_to_clean:
            del self._d[node]

    def __len__(self):
        return len(self._d)

    def __delitem__(self, node):
        node_id = NodeID.from_object(node)
        try:
            del self._d[node_id]
        except KeyError:
            pass

    def __getitem__(self, node_id):
        node_id = NodeID.from_object(node_id)
        return self._d[node_id]

    def __contains__(self, node):
        node_id = NodeID.from_object(node)
        return node_id in self._d

