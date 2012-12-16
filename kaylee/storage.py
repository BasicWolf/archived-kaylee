# -*- coding: utf-8 -*-
"""
    kaylee.storage
    ~~~~~~~~~~~~~~

    This module provides Kaylee storages' interfaces.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

from abc import ABCMeta, abstractmethod


class TemporalStorage(object):
    """The interface for applications' temporal results storage.

    Note that using this storage is to be decided by a controller.
    A controller may not need a temporal storage at all.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, node_id, task_id, result):
        """Stores the task result returned by a node."""

    @abstractmethod
    def remove(self, node_id, task_id):
        """Removes a particular task result returned by a defined node from
        the storage."""

    @abstractmethod
    def clear(self):
        """Removes all results from the storage."""

    @abstractmethod
    def keys(self):
        """Returns an iterator object of the storage keys (task ids)."""

    @abstractmethod
    def values(self):
        """Returns an iterator object of the storage values."""

    @abstractmethod
    def __len__(self):
        """Returns the total amount of results in the storage."""

    @abstractmethod
    def __getitem__(self, task_id):
        """Returns the task results.

        :rtype:  (node_id : result) ... iterator
        """

    @abstractmethod
    def __delitem__(self, task_id):
        """Removes all task results."""

    @abstractmethod
    def __contains__(self, task_id):
        """Checks if the task results are in the storage."""


class PermanentStorage(object):
    """The interface for applications' permanent results storage.
    The storage can be a file, a database, a Python object in memory etc.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, task_id, result):
        """Stores the task result."""

    @abstractmethod
    def keys(self):
        """Returns an iterator object of the storage keys (task ids)."""

    @abstractmethod
    def values(self):
        """Returns an iterator object of the storage values."""

    @abstractmethod
    def __len__(self):
        """Returns the total amount of results in the storage."""

    @abstractmethod
    def __getitem__(self, task_id):
        """Returns the task results.

        :rtype: :class:`list`
        """

    @abstractmethod
    def __contains__(self, task_id):
        """Checks if the task results are in the storage."""

    @abstractmethod
    def __iter__(self):
        """Returns the iterator object of the storage."""
