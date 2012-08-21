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

    def remove(self, node_id, task_id):
        del self._d[task_id][node_id]

    def clear(self):
        self._d = {}

    def __iter__(self):
        return iter(self._d)

    def __getitem__(self, task_id):
        try:
            return self._d[task_id]
        except KeyError:
            return []

    def __len__(self):
        return sum(len(res) for res in self._d)

    def __delitem__(self, task_id):
        del self._d[task_id]

    def __contains__(self, task_id):
        return task_id in self._d

    def keys(self):
        return self._d.iterkeys()

    def values(self):
        return self._d.itervalues()


class MemoryPermanentStorage(PermanentStorage):
    """A simple Python dict-based permanent results storage."""

    def __init__(self):
        self._d = {}
        self._count = 0

    def add(self, task_id, result):
        try:
            self._d[task_id].append(result)
        except KeyError:
            self._d[task_id] = [result, ]
        self._count += 1

    def keys(self):
        return self._d.iterkeys()

    def values(self):
        return self._d.itervalues()

    def __len__(self):
        return self._count

    def __getitem__(self, task_id):
        return self._d[task_id]

    def __contains__(self, task_id):
        return task_id in self._d

    def __iter__(self):
        return iter(self._d)
