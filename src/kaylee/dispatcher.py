# -*- coding: utf-8 -*-
import threading
from .objectid import NodeID
from .node import Node
from .errors import KayleeError


class Dispatcher(object):
    def __init__(self, applications, nodes_storage):
        """ """
        self.applications = applications
        self.nodes = nodes_storage
        self._lock = threading.Lock()

    def register(self, remote_host):
        """ """
        with self._lock:
            node = Node(NodeID(remote_host))
            self.nodes.add(node)
        return node.id

    def unregister(self, node_id):
        """ """
        self.nodes.remove(node_id)

    def subscribe(self, node_id, app):
        """ """
        try:
            node = self.nodes[node_id]
            return self.applications[app].subscribe(node)
        except KeyError:
            raise KayleeError('Node "{}" is not registered'.format(node_id))

    def unsubscribe(self, node_id):
        """ """
        raise NotImplementedError()

    def get_task(self, node_id):
        """ """
        node = self.nodes[node_id]

    def accept_results(self, node_id, data):
        """ """
        raise NotImplementedError()

    def clean(self):
        """The method removes all timed-out nodes from the dispatcher.
        """
        with self._lock:
            for node in self.nodes:
                pass
