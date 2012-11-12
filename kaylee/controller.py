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
from functools import wraps

from .util import AutoFilterABCMeta, BASE_FILTERS, CONFIG_FILTERS
from .errors import ApplicationCompletedError

#: The Application name regular expression pattern which can be used in
#: e.g. web frameworks' URL dispatchers.
app_name_pattern = r'[a-zA-Z\.\d_-]+'

#: Indicates active state of an application.
ACTIVE = 0x2
#: Indicates completed state of an application.
COMPLETED = 0x4

#  TODO: add link to kl.NO_SOLUTION

#: The { '__kl_result__' : NO_SOLUTION } result returned by the node
#: indicates that no solution was found for the given task. The controller
#: must take this information into account (see :func:`kl_result_filter`)
NO_SOLUTION = 0x2

#: The { '__kl_result__' : NEXT_TASK } solution returned by the node
#: indicates that the current task was simply not solved for some
#: reason, there are no results to accept and the node is asking for
#: the next task.
NEXT_TASK = 0x4

KL_RESULT = '__kl_result__'

def app_completed_guard(f):
    """The filter handles two cases of completed Kaylee application:

    1. First, it checks if the application has already completed and
       in that case immediately throws :exc:`ApplicationCompletedError`.
    2. Second, it wraps ``f`` in ``try..except`` block in order to
       set object's :attr:`Controller.completed` value to ``True``.
       After that :exc:`ApplicationCompletedError` is re-raised.

    .. note:: This is a base filter applied to :meth:`Controller.get_task`.
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.completed:
            raise ApplicationCompletedError(self.name)

        try:
            return f(self, *args, **kwargs)
        except ApplicationCompletedError as e:
            self.completed = True
            raise e
    return wrapper

def normalize_result_filter(f):
    """The filter normalizes the data before passing it further.

    .. note:: This is a base filter applied to :meth:`
              Controller.accept_result`.
    """
    @wraps(f)
    def wrapper(self, node, data):
        data = self.project.normalize_result(node.task_id, data)
        return f(self, node, data)
    return wrapper

def kl_result_filter(f):
    """The filter is designed to be used in "decision search" projects which
    imply that not every task has a correct solution, or solution exists at
    all.
    The filter searches for ``'__kl_result__'`` key in the result and acts
    according to the bound value:

    * :data:`NO_SOLUTION` : The result passed to the decorated function is
      turned to `None`. It can be ignored by :meth:`Project.store_result`
      routine.
    """
    @wraps(f)
    def wrapper(self, node, data):
        try:
            kl_result = data['__kl_result__']
        except (KeyError, TypeError):
            return f(self, node, data)

        if kl_result == NO_SOLUTION:
            data = None
            return f(self, node, data)
        elif kl_result == NEXT_TASK:
            return

    return wrapper


class Controller(object):
    """Controller is one of the main parts of Kaylee. A controller
    is a layer that binds projects and nodes. It dispatches the project tasks
    to nodes, and collects the results.

    A controller, a project, a temporal and permanenet storages altogether
    form a *Kaylee Application*.

    Metaclass: :class:`AutoFilterABCMeta <kaylee.util.AutoFilterABCMeta>`.

    :param name: Application name.
    :param project: Bound project.
    :param storage: Internal storage for storing intermediate (temporal)
                    results before storing them to a permanent storage.
    :type name: string
    :type project: :class:`Project`
    :type storage: :class:`TemporalStorage`
    """
    __metaclass__ = AutoFilterABCMeta

    auto_filter = BASE_FILTERS | CONFIG_FILTERS
    auto_filters = {
        'get_task' : [app_completed_guard, ],
        'accept_result' : [normalize_result_filter, app_completed_guard]
        }

    _app_name_re = re.compile('^{}$'.format(app_name_pattern))

    def __init__(self, name, project, storage = None, *args, **kwargs):
        if Controller._app_name_re.match(name) is None:
            raise ValueError('Invalid application name: {}'
                             .format(name))
        self.name = name
        self.project = project
        self.storage = storage
        self._state = ACTIVE

    @app_completed_guard
    def subscribe(self, node):
        """Subscribes a node for current application.

        :param node: A registered node.
        :type node: :class:`Node`
        """
        node.controller = self
        node.subscription_timestamp = datetime.now()
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
