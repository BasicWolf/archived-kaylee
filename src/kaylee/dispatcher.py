# -*- coding: utf-8 -*-
import threading
from .objectid import NodeID
from .node import Node
from .controller import load_applications
from .errors import KayleeError
from .storage import MemoryNodesStorage

class Dispatcher(object):
    def __init__(self):
        self.controllers = load_applications()

    def register(self, remote_host):
        pass

    def unregister(self, nid):
        pass

    def subscribe(self, nid, app):
        pass

    def unsubscribe(self, nid):
        pass

    def get_task(self, nid):
        pass

    def accept_results(self, nid, data):
        pass

    def clean(self):
        """The method removes all timed-out nodes from the dispatcher.
        """

class DefaultDispatcher(Dispatcher):
    def __init__(self):
        super(DefaultDispatcher, self).__init__()
        self.nodes = MemoryNodesStorage()
        self._lock = threading.Lock()

    def register(self, remote_host):
        with self._lock:
            node = Node(NodeID(remote_host))
            self.nodes.add(node)
        return node.id

    def unregister(self, nid):
        pass

    def subscribe(self, nid, app):
        if nid in self.nodes:
            return self.controllers[app].subscribe(nid)
        raise KayleeError('Node "{}" is not registered'.format(nid))

    def unsubscribe(self, nid):
        pass

    def get_task(self, nid):
        pass

    def accept_results(self, nid, data):
        pass

    def clean(self):
        with self._lock:
            for node in self.nodes:
                pass
