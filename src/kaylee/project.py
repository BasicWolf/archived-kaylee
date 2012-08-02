# -*- coding: utf-8 -*-
"""
    kaylee.project
    ~~~~~~~~~~~~~~

    This module provides basic interfaces for Kaylee projects.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""
from abc import abstractmethod
from copy import copy
from functools import wraps

from .util import AutoFilterABCMeta


DEPLETED = 0x2
COMPLETED = 0x4

def depleted_guard(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except StopIteration as e:
            self.depleted = True
            raise e
    return wrapper

def ignore_null_result(f):
    @wraps(f)
    def wrapper(self, data):
        if data is not None:
            return f(self, data)
        return None
    return wrapper


class ProjectMeta(AutoFilterABCMeta):
    auto_filters = {
        '__next__' : [ depleted_guard, ],
        'normalize' : [ ignore_null_result, ],
       }


class Project(object):
    """Base class for Kaylee projects. Essentialy a Project is an
    iterator that yields Kaylee Tasks.

    Every :class:`Task` has a unique id and a project should be able
    to return the same task by given id if required.

    Project supports auto filters. (TODO)
    """

    __metaclass__ = ProjectMeta
    auto_filter = False

    def __init__(self, storage = None, *args, **kwargs):
        #: A dictionary with configuration
        #: details used by every client-side node. For example, it can
        #: contain a path to the javascript file with project's
        #: client-side logic. That path will be later used by Kaylee's
        #: client engine to load and start calculations on client.
        #: TODO
        self.client_config = {
            'script' : kwargs['script'],
            }
        self.storage = storage
        self._state = 0

    def next(self):
        """Same as :meth:`__next__` ."""
        return self.__next__()

    @abstractmethod
    def __next__(self):
        """
        Returns the next task. In case if ``__next__()`` throws
        :exc:`StopIteration`, it means that there will be no more
        new tasks from the project, but the bound controller can still
        refer to old tasks via project[task_id]. After :exc:`StopIteration`
        has been thrown, :attr:`depleted` **must** be set (by the project or
        via filter) to `True`.
        In case that :class:`Controller` does not intercept or re-throw
        :exc:`StopIteration`, :class:`Kaylee` catches and interprets it as
        "no need to involve the bound node in any further calculations for
        the application".

        :throws: StopIteration
        :returns: an instance of :class:`Task`
        """

    @abstractmethod
    def __getitem__(self, task_id):
        """Returns task with the required id."""

    @property
    def depleted(self):
        """Indicates if current project instance has run out of new tasks."""
        return self._state & DEPLETED

    @depleted.setter
    def depleted(self, val):
        if val:
            self._state |= DEPLETED
        else:
            self._state &= ~DEPLETED

    @property
    def completed(self):
        """Indicates if current project instance was completed."""
        return self._state & COMPLETED

    @completed.setter
    def completed(self, val):
        if val:
            self._state |= COMPLETED
        else:
            self._state &= ~COMPLETED

    def normalize(self, data):
        """Normalizes and validates the reply from a node.

        :param data: the data to be validated and/or normalized.
        :throws ValueError: in case of invalid result.
        :return: normalized data.
        """
        return data

    def store_result(self, task_id, data):
        """Accepts and processes results from a node.

        :param task_id: ID of the task
        :param data: Results of the task. The results are parsed from the
                     JSON data returned by the node.
                     By-default the ``None`` result is not stored
                     to the storage.
        :type data: dict, list or None
        """
        if data is not None:
            self.storage[task_id] = data


class TaskMeta(type):
    """
    The metaclass for :class:`Task`. Adds **serializable**
    attribute logic to the class. This attribute is a list
    which contains the names of the Task's attributes that
    are stored into a dictionary which is then returned
    by the serialize() method. This dictionary can be used to
    e.g. export the object to JSON.
    """
    def __new__(meta, classname, bases, class_dict):
        serializable = []
        if 'serializable' in class_dict:
            serializable = class_dict['serializable']

        for base in bases:
            if hasattr(base, 'serializable'):
                # extend from left side of the list
                serializable[:-len(serializable)] = base.serializable
        class_dict['serializable'] = serializable
        return type.__new__(meta, classname, bases, class_dict)


class Task(object):
    """
    Base class for Kaylee projects' tasks. This class is meant to be
    inherited in users' projects if additional attributes-to-be-serialized
    are required. When serialized, Task.id is converted to string,
    whereas other attributes' values are stored unmodified.
    For example::

        class MyTask(Task):
            serializable = ['speed']

            def __init__(self, task_id, speed):
                super(MyTask, self).__init__(task_id)
                self.speed = speed

        task = MyTask('001', 60)
        task.serialize()
        # >>> { 'id' : '001', 'speed' : 60 }


    :param task_id: Unique task id.
    :type task_id: string
    """
    __metaclass__ = TaskMeta
    serializable = ['id']

    def __init__(self, task_id):
        self.id = str(task_id)

    def serialize(self, attributes = None):
        """
        Serializes object attributes to dict.

        :param attributes: A custom list of attributes which overrides
                           ``self.serializable``.
        """
        if attributes is None:
            attributes = self.serializable
        return { attr : getattr(self, attr) for attr in attributes }

    def __str__(self):
        return 'Task: ' + '; '.join('{0}: {1}'.format(attr, getattr(self, attr))
                                    for attr in self.serializable )
