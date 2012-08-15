from kaylee.storage import TemporalStorage, PermanentStorage
from kaylee.errors import KayleeError

class MemoryTemporalStorage(TemporalStorage):
    """A simple Python dict-based temporal results storage."""

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


class MemoryPermanentStorage(PermanentStorage):
    """A simple Python dict-based permanent results storage."""

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
