# -*- coding: utf-8 -*-
#pylint: disable-msg=W0231
from kaylee.storage import TemporalStorage, PermanentStorage

class MemoryTemporalStorage(TemporalStorage):
    """A simple Python dict-based temporal results storage."""

    def __init__(self):
        self._d = {}
        self.clear()

    def add(self, task_id, node_id, result):
        d = self._d.get(task_id, {})
        d[node_id] = result
        self._d[task_id] = d

    def remove(self, task_id, node_id=None):
        if node_id is None:
            del self._[task_id]
        else:
            del self._d[task_id][node_id]

    def clear(self):
        self._d = {}

    def __getitem__(self, task_id):
        try:
            return self._d[task_id]
        except KeyError:
            return []

    def contains(self, task_id, node_id=None, result=None):
        if result is None and node_id is None:
            return task_id in self._d
        elif result is None:
            return node_id in self._d[task_id]
        else:
            return result in self._d[task_id][node_id]

    @property
    def count(self):
        pass

    @property
    def total_count(self):
        pass

    def keys(self):
        return self._d.iterkeys()

    def values(self):
        def node_result_tuple_generator():
            for nr_dict in self._d.itervalues():
                for node_id, result in nr_dict:
                    # in Py3 yield from would be proper here
                    yield (node_id, result)
        return node_result_tupe_generator()

    def __contains__(self, task_id):
        return task_id in self._d

    def __delitem__(self, task_id):
        del self._d[task_id]

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return sum(len(res) for res in self._d)


class MemoryPermanentStorage(PermanentStorage):
    """A simple Python dict-based permanent results storage."""

    def __init__(self):
        self._d = {}
        self._total_count = 0

    def add(self, task_id, result):
        try:
            self._d[task_id].append(result)
        except KeyError:
            self._d[task_id] = [result, ]
        self._total_count += 1

    def __getitem__(self, task_id):
        return self._d[task_id]

    def contains(self, task_id, result = None):
        if result is None:
            return task_id in self._d
        else:
            return task_id in self._d and result in self._d[task_id]

    def keys(self):
        return self._d.iterkeys()

    def values(self):
        return self._d.itervalues()

    @property
    def count(self):
        return len(self._d)

    @property
    def total_count(self):
        return self._total_count
