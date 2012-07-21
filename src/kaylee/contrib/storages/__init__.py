from kaylee.storage import (NodesStorage, ControllerResultsStorage,
                            ProjectResultsStorage)

from kaylee.errors import KayleeError
from kaylee.node import Node, NodeID
from kaylee.util import parse_timedelta


class MemoryNodesStorage(NodesStorage):
    def __init__(self, timeout, *args, **kwargs):
        self._d = {}
        self.timeout = parse_timedelta(timeout)
        super(MemoryNodesStorage, self).__init__(*args, **kwargs)

    def add(self, node):
        self._d[node.id] = node

    def clean(self):
        nodes_to_clean = [node for node in self._d.iteritems()
                          if datetime.now() - node.id.timestamp > self.timeout]
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


class MemoryControllerResultsStorage(ControllerResultsStorage):
    def __init__(self):
        self.clear()

    def add(self, node_id, task_id, result):
        d = self._d.get(task_id, {})
        d[node_id] = result
        self._d[task_id] = d
        self._dirty = True

    def remove(self, node_id, task_id):
        del self._d[task_id][node_id]
        self._dirty = True

    def clear(self):
        self._d = {}
        self._count = 0
        self._dirty = True

    def __getitem__(self, task_id):
        try:
            return self._d[task_id]
        except KeyError:
            return []

    def __len__(self):
        if self._dirty:
            self._count = sum(len(res) for res in self._d)
            self._dirty = False
        return self._count

    def __setitem__(self, task_id, val):
        self._d[task_id] = val

    def __delitem__(self, task_id):
        self._dirty = True
        del self._d[task_id]

    def __contains__(self, task_id):
        return task_id in self._d


class MemoryProjectResultsStorage(ProjectResultsStorage):
    def __init__(self):
        self._d = {}
        self._count = 0

    def __len__(self):
        return self._count

    def __delitem__(self, task_id):
        self._count -= len(self._d[task_id])
        del self._d[task_id]

    def __getitem__(self, task_id):
        return self._d[task_id]

    def __setitem__(self, task_id, result):
        if not isinstance(result, list):
            result = [result]
        self._d[task_id] = result
        self._count += len(result)

    def __contains__(self, task_id):
        return task_id in self._d

    def __iter__(self):
        return iter(self._d)

    def keys(self):
        return self._d.iterkeys()

    def values(self):
        return self._d.itervalues()
