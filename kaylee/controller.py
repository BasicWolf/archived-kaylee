# -*- coding: utf-8 -*-
"""
    kaylee.controller
    ~~~~~~~~~~~~~~~~~

    This module provides classes for Kaylee controllers.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

import re
from abc import ABCMeta, abstractmethod

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
    """A Controller object maintains the data (tasks and the results) flow
    between a project the outer :class:`Kaylee` interface and the storages.
    An instance of ``Controller`` with a bound project and storages forms
    a *Kaylee Application*.

    :param name: application name
    :param project: bound project
    :param permanent_storage: permanent application results storage
    :param temporal_storage: internal storage for storing intermediate
                             (temporal) results
    :type name: string
    :type project: :class:`Project`
    :type permanent_storage: :class:`PermanentStorage`
    :type temporal_storage: :class:`TemporalStorage`
    """
    __metaclass__ = ABCMeta

    _app_name_re = re.compile('^{}$'.format(app_name_pattern))

    def __init__(self, name, project, permanent_storage,
                 temporal_storage=None):
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
        :type node: :class:`Node`
        :throws ApplicationCompletedError: if the application is completed.
        """

    @abstractmethod
    def accept_result(self, node, result):
        """Accepts and processes the results from a node.

        :param node: Kaylee Node from which the results have been received.
        :param result: JSON-parsed task results.
        :type result: :class:`dict` or :class:`list`
        """

    def store_result(self, task_id, result):
        """Stores the result to permanent storage and notifies the bound
        project."""
        self.permanent_storage.add(task_id, result)
        self.project.result_stored(task_id, result, self.permanent_storage)

    @property
    def completed(self):
        """Indicates whether the application is completed."""
        return self._state & COMPLETED == COMPLETED

    @completed.setter
    def completed(self, val):
        if val:
            self._state |= COMPLETED
        else:
            self._state &= ~COMPLETED

    def __hash__(self):
        return hash(self.name)
