# -*- coding: utf-8 -*-
"""
    kaylee.contrib.storages
    ~~~~~~~~~~~~~~~~~~~~~~~

    The module provides basic Kaylee storages' implementations.

    :copyright: (c) 2013 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""
#pylint: disable-msg=W0231

from kaylee.storage import TemporalStorage, PermanentStorage
from kaylee.node import NodeID

class MemoryTemporalStorage(TemporalStorage):
    """A simple Python dict-based temporal results storage."""

    def __init__(self):
        self._d = {}
        self.clear()
        self._total_count = 0

    def add(self, task_id, node_id, result):
        d = self._d.get(task_id, {})
        d[node_id.binary] = result
        self._d[task_id] = d
        self._total_count += 1

    def remove(self, task_id, node_id=None):
        if node_id is None:
            deleted_results = self._d.pop(task_id)
            self._total_count -= len(deleted_results)
        else:
            del self._d[task_id][node_id]
            self._total_count -= 1

    def clear(self):
        self._d = {}
        self._total_count = 0

    def __getitem__(self, task_id):
        nr_dict = self._d[task_id]
        return ((NodeID(n), r) for n, r in nr_dict.iteritems())

    def contains(self, task_id, node_id=None, result=None):
        try:
            if result is None and node_id is None:
                return task_id in self._d
            elif result is None:
                return node_id in self._d[task_id]
            else:
                return result in self._d[task_id][node_id]
        except KeyError:
            return False

    @property
    def count(self):
        return len(self._d)

    @property
    def total_count(self):
        return self._total_count

    def keys(self):
        return self._d.iterkeys()

    def values(self):
        def node_result_tuple_generator():
            for nr_dict in self._d.itervalues():
                for nid_res_tuple in nr_dict.iteritems():
                    # in Py3 yield from would be proper here
                    yield nid_res_tuple
        return node_result_tuple_generator()


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
