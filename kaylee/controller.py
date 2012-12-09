# -*- coding: utf-8 -*-
"""
    kaylee.controller
    ~~~~~~~~~~~~~~~~~

    This module provides classes for Kaylee controllers.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

import re
from abc import abstractmethod, abstractproperty
from datetime import datetime
from .errors import ApplicationCompletedError

#: The Application name regular expression pattern which can be used in
#: e.g. web frameworks' URL dispatchers.
app_name_pattern = r'[a-zA-Z\.\d_-]+'

#: Indicates active state of an application.
ACTIVE = 0x2
#: Indicates completed state of an application.
COMPLETED = 0x4

KL_RESULT = '__klr__'

#: The ``NO_SOLUTION`` result returned by the node indicates that no solution
#: was found for the given task. The controller must take this information
#: into account.
NO_SOLUTION = { KL_RESULT : 0x2 }

#: The ``NOT_SOLVED`` result returned by the node indicates that the current
#: task was simply not solved for some reason and there are no results to
#: accept.
NOT_SOLVED = { KL_RESULT : 0x4 }


class Controller(object):
    """Controller is one of the main parts of Kaylee. A controller
    is a layer that binds projects and nodes. It dispatches the project tasks
    to nodes, and collects the results.

    A controller, a project, a temporal and permanenet storages altogether
    form a *Kaylee Application*.

    TODOC

    :param name: Application name.
    :param project: Bound project.
    :param temporal_storage: Internal storage for storing intermediate
                             (temporal) results before storing them to
                             a permanent storage.
    :type name: string
    :type project: :class:`Project`
    :type temporal_storage: :class:`TemporalStorage`
    """

    _app_name_re = re.compile('^{}$'.format(app_name_pattern))

    def __init__(self, name, project, permanent_storage,
                 temporal_storage = None, *args, **kwargs):
        if Controller._app_name_re.match(name) is None:
            raise ValueError('Invalid application name: {}'
                             .format(name))
        self.name = name
        self.project = project
        self.permanent_storage = permanent_storage
        self.temporal_storage = temporal_storage
        self._state = ACTIVE

    @abstractmethod
    def get_task(self, node):
        """Returns a task for the node.

        :param node: Kaylee Node requesting the task for computation.
        :throws: :class:`ApplicationCompletedError` if application has been
                 completed.
        """

    @abstractmethod
    def accept_result(self, node, result):
        """Accepts and processes results from a node.

        :param node: Kaylee Node from which the results have been received.
        :param result: JSON-parsed task results.
        :type result: dict or list
        """

    def store_result(self, task_id, result):
        """Stores the result to permanent storage and notifies the bound
        project."""
        self.permanent_storage.add(task_id, result)
        self.project.result_stored(task_id, result, self.permanent_storage)

    @property
    def completed(self):
        """Indicates if application was completed."""
        return self._state & COMPLETED == COMPLETED

    @completed.setter
    def completed(self, val):
        if val:
            self._state |= COMPLETED
        else:
            self._state &= ~COMPLETED

    def __hash__(self):
        return hash(self.name)
