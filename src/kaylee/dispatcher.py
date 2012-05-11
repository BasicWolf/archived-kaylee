import threading
from .objectid import NodeID
from .node import Node


class Dispatcher(object):
    def register(self, remote_host):
        pass

    def unregister(self, nid):
        pass

    def subscribe(self, nid, project):
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
        self.nodes = set()
        self._lock = threading.Lock()

    def register(self, remote_host):
        with self._lock:
            node = Node(NodeID(remote_host) )
            self.nodes.add(node)
        return node.id

    def unregister(self, nid):
        pass

    def subscribe(self, nid, project):
        pass

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
