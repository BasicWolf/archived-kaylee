# -*- coding: utf-8 -*-
"""
    kaylee.project
    ~~~~~~~~~~~~~~

    This module provides basic interfaces for Kaylee projects.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT or GPLv3, see LICENSE for more details.
"""
from abc import ABCMeta, abstractmethod
from copy import copy


class Project(object):
    """Base class for Kaylee projects. Essentialy a Project is an
    iterator that yields Tasks. Every task has a unique id and a
    project should be able to return the same task on
    when project.__getitem__(same_id) is called."""

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        #: Project.node_config is a dictionary with configuration
        #: details used by every client-side node. For example, it can
        #: contain a path to the javascript file with project's
        #: client-side logic. That path will be later used by Kaylee's
        #: client engine to load and start calculations on client.
        self.nodes_config = { }

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    @abstractmethod
    def __next__(self):
        """Returns the next task."""

    @abstractmethod
    def __getitem__(self, task_id):
        """Returns task with required id."""

    def normalize(self, data):
        """Normalizes and validates the reply from a node.

        :param data: the data to be validated and/or normalized.
        :throws InvlaidResultError: in case of invalid result.
        :return: normalized data.
        """
        return data


class TaskMeta(type):
    """
    Metaclass for kaylee.project.Task. Adds 'serializable' incremental
    list logic to the class. The serializable field of a class is a list
    which contains the names of the object fields that will be put
    into a dictionary and returned by the serialize() method.
    This dictionary can be then used to e.g. dump the object to JSON.
    """
    def __new__(meta, classname, bases, class_dict):
        serializable = []
        if 'serializable' in class_dict:
            serializable = class_dict['serializable']

        for base in bases:
            if hasattr(base, 'serializable'):
                serializable.extend(base.serializable)
        class_dict['serializable'] = serializable
        return type.__new__(meta, classname, bases, class_dict)


class Task(object):
    """
    Base class for Kaylee projects' tasks. This class is meant to be
    inherited in users' projects if additional fields-to-be-serialized
    are required. When serialized Task.id is converted to string,
    whereas other fields' values are stored unmodified. For example:

    class MyTask(Task):

        serializable = ['speed']

        def __init__(self, task_id, speed):
            super(MyTask, self).__init__(task_id)
            self.speed = speed


    task = MyTask('001', 60)
    task.serialize()
    >>> { 'id' : '001', 'speed' : 60 }
    """
    serializable = ['id']

    def __init__(self, task_id):
        self.id = str(task_id)

    def serialize(self):
        """
        Serializes object fields to dictionary. The serialized fields
        are taken from self.serializable list.
        """
        return { key : self.__dict__[key] for key in self.serializable }
