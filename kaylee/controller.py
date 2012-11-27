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

from .util import AutoFilterABCMeta, BASE_FILTERS, CONFIG_FILTERS
from .errors import ApplicationCompletedError
from .filters import (normalize_result, app_completed_guard,
                      ignore_null_result)

#: The Application name regular expression pattern which can be used in
#: e.g. web frameworks' URL dispatchers.
app_name_pattern = r'[a-zA-Z\.\d_-]+'

#: Indicates active state of an application.
ACTIVE = 0x2
#: Indicates completed state of an application.
COMPLETED = 0x4


class Controller(object):
    """Controller is one of the main parts of Kaylee. A controller
    is a layer that binds projects and nodes. It dispatches the project tasks
    to nodes, and collects the results.

    A controller, a project, a temporal and permanenet storages altogether
    form a *Kaylee Application*.

    Metaclass: :class:`AutoFilterABCMeta <kaylee.util.AutoFilterABCMeta>`.

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
    __metaclass__ = AutoFilterABCMeta

    auto_filter = BASE_FILTERS | CONFIG_FILTERS
    auto_filters = {
        'get_task' : [app_completed_guard, ],
        'accept_result' : [normalize_result, app_completed_guard],
        'store_result' : [ignore_null_result],
    }

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

    @app_completed_guard
    def subscribe(self, node):
        """Subscribes the node for current application.

        :param node: A registered node.
        :type node: :class:`Node`
        """
        node.subscribe(self)
        return self.project.client_config

    @abstractmethod
    def get_task(self, node):
        """Returns a task for a node."""

    @abstractmethod
    def accept_result(self, node, data):
        """Accepts and processes results from a node.

        :param node: Active Kaylee Node from which the results are received.
        :param data: JSON-parsed task results.
        :type data: dict or list
        """

    def store_result(self, task_id, data):
        """Stores the result to permanent storage and notifies the bound
        project."""
        self.permanent_storage.add(task_id, data)
        self.project.result_stored(task_id, data, self.permanent_storage)

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
