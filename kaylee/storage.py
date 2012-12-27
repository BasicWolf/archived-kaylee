# -*- coding: utf-8 -*-
"""
    kaylee.storage
    ~~~~~~~~~~~~~~

    This module provides Kaylee storages' interfaces.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

from abc import ABCMeta, abstractmethod, abstractproperty


class TemporalStorage(object):
    """The interface for applications' temporal results storage.

    Note that using this storage is to be decided by a controller.
    A controller may not need a temporal storage at all.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, task_id, node_id, result):
        """Stores the task result returned by a node."""

    @abstractmethod
    def remove(self, task_id, node_id):
        """Removes a particular task result returned by a defined node from
        the storage."""

    @abstractmethod
    def clear(self):
        """Removes all results from the storage."""

    @abstractmethod
    def __getitem__(self, task_id):
        """Returns the task results.

        :rtype:  (node_id : result) ... iterator
        """

    @abstractmethod
    def contains(self, task_id, node_id=None, result=None):
        """Checks if any of the task results or a result from a node or a
        particular task result is contained in the storage"""
        pass

    @abstractmethod
    def count(self):
        """Returns the amount of results in the storage.
        This is the same as:: ``len(list(ts.keys()))``, where ``ts`` is an
        instance of :class:`TemporalStorage`."""

    @abstractmethod
    def values(self):
        """Returns the stored results iterator object. Each yield item is
        a ``(node_id, result)`` tuple."""

    @abstractmethod
    def keys(self):
        """Returns the stored tasks iterator object of the storage. Each
        yield item is a task ID."""

    def __contains__(self, task_id):
        """Checks if any of the task results are in the storage.
        Same as :meth:`PermanentStorage.contains(task_id)
        <PermanentStorage.contains>`."""
        return self.contains(task_id)

    def __delitem__(self, task_id):
        """Removes all task results from the storage. This is the same as
        ``ts.remove(task_id)`` where ``ts`` is an instance of
        :class:`TemporalStorage`."""
        self.remove(task_id)

    def __iter__(self):
        """The same as :meth:`TemporalStorage.keys`."""
        return self.keys()

    def __len__(self):
        """The same as ``len(ts)`` where ``ts`` is an instance of
        :class:`TemporalStorage`"""


class PermanentStorage(object):
    """The interface for applications' permanent results storage.
    The storage can be a file, a database, a Python object in memory etc.

    The idea of the storage to store the tasks' results in the following
    fashion::

      {
          task_id1 : [res11, res12, ...],
          task_id2 : [res21, res22, ...],
          ...
      }

    Thus, :meth:`PermanentStorage.add(task_id, result) <PermanentStorage.add>`
    Initially adds the results to the storage, and appends the results if
    called the second, the third etc. time with the same ``task_id`` argument.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, task_id, result):
        """Stores the task result."""

    @abstractmethod
    def __getitem__(self, task_id):
        """Returns a list of task results.

        :rtype: :class:`list`
        """

    @abstracmethod
    def contains(self, task_id, result = None):
        """Checks if any of the task results or a particular task result
        is contained in the storage"""

    @abstractmethod
    def values(self):
        """Returns the stored results iterator object. Each yield item is
        a list of results associated with a particular task."""

    @abstractmethod
    def keys(self):
        """Returns the stored tasks iterator object of the storage. Each
        yield item is a task ID."""

    @abstractproperty
    def count(self):
        """Returns the amount of tasks' results in the storage.
        This is the same as:: ``len(list(ps.keys()))``, where ``ps`` is an
        instance of :class:`PermanentStorage`.
        """
        pass

    @abstractproperty
    def total_count(self):
        pass

    def __contains__(self, task_id):
        """Checks if any of the task results are in the storage.
        Same as :meth:`PermanentStorage.contains(task_id)
        <PermanentStorage.contains>`."""
        return self.contains(task_id)

    def __iter__(self):
        """The same as :meth:`PermanentStorage.keys`."""
        return self.keys

    def __len__(self):
        """Same as :meth:`PermanentStorage.count`."""
        return self.count
