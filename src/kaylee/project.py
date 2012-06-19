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
from .util import AutoFilterABCMeta

def depleted_guard(f):
    def wrapper(obj, *args, **kwargs):
        try:
            return f(obj, *args, **kwargs)
        except StopIteration as e:
            obj._depleted = True
            raise e
    return wrapper


class ProjectMeta(AutoFilterABCMeta):
    _filters = {
        '__next__' : [depleted_guard, ]
        }


class Project(object):
    """Base class for Kaylee projects. Essentialy a Project is an
    iterator-like object that yields Tasks. A common project supports
    next() calls but does not implement the __iter__() method. Thus, all
    iteration variables should be initialized in the __init__() method.

    Every task has a unique id and a project should be able to return the
    same task when project.__getitem__(same_id) is called."""

    __metaclass__ = ProjectMeta
    auto_filter = True

    def __init__(self, *args, **kwargs):
        #: Project.node_config is a dictionary with configuration
        #: details used by every client-side node. For example, it can
        #: contain a path to the javascript file with project's
        #: client-side logic. That path will be later used by Kaylee's
        #: client engine to load and start calculations on client.
        self.nodes_config = {
            'script' : kwargs['script'],
            }
        self._depleted = False

    def next(self):
        return self.__next__()

    @abstractmethod
    def __next__(self):
        """
        Returns the next task. In case if __next__() throws StopIteration,
        it means that there will be no more new tasks from the project,
        but the bound controller can still refer to old tasks via
        project[task_id]. After StopIteration has been thrown,
        :attr:`Project.depleted` **must** return True.
        In case that :class:`Controller` does not intercept or re-throws
        StopIteration, :class:`Kaylee` catches and interprets it as no
        need to involve the bound node in any further calculations for
        the application.

        :throws: StopIteration
        """

    @abstractmethod
    def __getitem__(self, task_id):
        """Returns task with the required id."""

    @property
    def depleted(self):
        return self._depleted

    def normalize(self, data):
        """Normalizes and validates the reply from a node.

        :param data: the data to be validated and/or normalized.
        :throws ValueError: in case of invalid result.
        :return: normalized data.
        """
        return data


class TaskMeta(type):
    """
    The Metaclass for :class:`kaylee.project.Task`. Adds 'serializable'
    incremental list logic to the class. The serializable attributes
    of the class is a list which contains the names of the objects'
    attributes that are put into a dictionary which is then returned
    by the serialize() method. This dictionary can be then used to
    e.g. dump the object to JSON.
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
    are required. When serialized Task.id is converted to string,
    whereas other attributes' values are stored unmodified. For example:

    class MyTask(Task):

        serializable = ['speed']

        def __init__(self, task_id, speed):
            super(MyTask, self).__init__(task_id)
            self.speed = speed

    task = MyTask('001', 60)
    task.serialize()
    >>> { 'id' : '001', 'speed' : 60 }
    """
    __metaclass__ = TaskMeta
    serializable = ['id']

    def __init__(self, task_id):
        self.id = str(task_id)

    def serialize(self):
        """
        Serializes object attributes to dictionary. The serialized fields
        are taken from self.serializable list.
        """
        return { attr : getattr(self, attr) for attr in self.serializable }

    def __str__(self):
        return 'Task: ' + '; '.join('{0}: {1}'.format(attr, getattr(self, attr))
                                    for attr in self.serializable )
