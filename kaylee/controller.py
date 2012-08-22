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
from .errors import StopApplication

#: The Application name regular expression pattern which can be used in
#: e.g. web frameworks' URL dispatchers.
app_name_pattern = r'[a-zA-Z\.\d_-]+'

#: Indicates active state of an application.
ACTIVE = 0x2
#: Indicates completed state of an application.
COMPLETED = 0x4


def app_completed_guard(f):
    """The filter handles two cases of completed Kaylee application:

    1. First, it checks if the application has already completed and
       in that case raises :exc:`StopApplication`.
    2. Second, it wraps ``f`` in ``try..except`` block in order to
       set object's :attr:`Controller.completed` value to ``True``.
       The :exc:`StopApplication` is then re-raised.

    .. note:: This is a base filter applied to :meth:`Controller.get_task`.
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.completed:
            raise StopApplication(self.app_name)
        try:
            return f(self, *args, **kwargs)
        except StopApplication as e:
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
        data = self.project.normalize(node.task_id, data)
        return f(self, node, data)
    return wrapper

def failed_result_filter(f):
    """The filter is meant to be used in "decision search" projects which
    supposed to deliver a single correct result.
    It converts the ``{ '__kl_result__' : False }`` result to ``None``,
    which should be ignored by projects' :meth:`Project.store_result` routine.
    """
    @wraps(f)
    def wrapper(self, node, data):
        try:
            if data['__kl_result__'] == False:
                data = None
        except KeyError:
            pass
        return f(self, node, data)
    return wrapper


class Controller(object):
    """Controller is one of the main parts of Kaylee. A controller
    is a layer that binds projects and nodes. It dispatches the project tasks
    to nodes, and collects the results.

    A controller, a project, a temporal and permanenet storages altogether
    form a *Kaylee Application*.

    Metaclass: :class:`AutoFilterABCMeta <kaylee.util.AutoFilterABCMeta>`.

    :param app_name: Application name.
    :param project: Bound project.
    :param storage: Internal storage for storing intermediate (temporal)
                    results before storing them to a permanent storage.
    :type app_name: string
    :type project: :class:`Project`
    :type storage: :class:`TemporalStorage`
    """
    __metaclass__ = AutoFilterABCMeta

    auto_filter = BASE_FILTERS | CONFIG_FILTERS
    auto_filters = {
        'get_task' : [app_completed_guard, ],
        'accept_result' : [normalize_result_filter, ]
        }

    _app_name_re = re.compile('^{}$'.format(app_name_pattern))

    def __init__(self, app_name, project, storage = None, *args, **kwargs):
        if Controller._app_name_re.match(app_name) is None:
            raise ValueError('Invalid application name: {}'
                             .format(app_name))
        self.app_name = app_name
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
        """Returns a task for a node.

        :throws errors.StopApplication:
        """

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
        return self._state & COMPLETED

    @completed.setter
    def completed(self, val):
        if val:
            self._state |= COMPLETED
        else:
            self._state &= ~COMPLETED

    def __hash__(self):
        return hash(self.app_name)
