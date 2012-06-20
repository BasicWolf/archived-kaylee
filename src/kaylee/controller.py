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

from .node import Node
from .util import AutoFilterABCMeta
from .errors import AppCompletedError

#: The Application name regular expression pattern which can be used in
#: e.g. web frameworks' URL dispatchers.
app_name_pattern = r'[a-zA-Z\.\d_-]+'
_app_name_re = re.compile('^{}$'.format(app_name_pattern))

#: Indicates active state of an application.
ACTIVE = 0x2
#: Indicates completed state of an application.
COMPLETED = 0x4


def app_completed_guard(f):
    """This decorator handles two cases of completed Kaylee application:

    1. First, it checks if the application has already completed and
       in that case raises :exc:`AppCompletedError`.
    2. Second, it wraps ``f`` in ``try..except`` block in order to
       set object's :attr:`Controller.state` value to :data:`COMPLETED`.
       The :exc:`AppCompletedError` is then re-raised.
    """
    def wrapper(obj, *args, **kwargs):
        if obj.state == COMPLETED:
            raise AppCompletedError(obj.app_name)
        try:
            return f(obj, *args, **kwargs)
        except AppCompletedError as e:
            obj.state = COMPLETED
            raise e
    return wrapper

def normalize_result_filter(f):
    def wrapper(self, node, data):
        data = self.project.normalize(data)
        return f(self, node, data)
    return wrapper

def failed_result_filter(f):
    def wrapper(self, node, data):
        try:
            if data['__kl_result__'] == False:
                data = None
        except KeyError:
            pass
        return f(self, node, data)
    return wrapper


class ControllerMeta(AutoFilterABCMeta):
    _filters = {
        'get_task' : [
            app_completed_guard,
            ],
        'accept_result' : [
            normalize_result_filter,
            ]
        }


class Controller(object):
    __metaclass__ = ControllerMeta
    auto_filter = True

    def __init__(self, id, app_name, project, storage, *args, **kwargs):
        if _app_name_re.match(app_name) is None:
            raise ValueError('Invalid application name: {}'
                             .format(app_name))
        self.id = id
        self.app_name = app_name
        self.project = project
        self.storage = storage
        self.state = ACTIVE

    @app_completed_guard
    def subscribe(self, node):
        """Subscribes a node for bound project."""
        node.controller = self
        node.subscription_timestamp = datetime.now()
        return self.project.nodes_config

    @abstractmethod
    def get_task(self, node):
        """ """

    @abstractmethod
    def accept_result(self, node, data):
        """Accepts and processes results from a node.

        :param node: Active Kaylee Node from which the results are received.
        :param data: Results of the task performed by the node.
        :type data:  JSON-parsed data (``dict`` or ``list``).
        """


class SimpleController(Controller):
    def __init__(self, *args, **kwargs):
        super(SimpleController, self).__init__(*args, **kwargs)
        self._tasks_pool = set()

    def get_task(self, node):
        if not self.project.depleted:
            try:
                task = next(self.project)
            except StopIteration:
                # at this point, project.depleted is expected
                # to become 'True'
                pass

        if self.project.depleted:
            try:
                tp_id = self._tasks_pool.pop()
                task = self.project[tp_id]
            except KeyError:
                # project depleted and nothing in the pool,
                # looks like the application has completed.
                raise AppCompletedError(self.app_name)

        node.task_id = task.id
        self._tasks_pool.add(task.id)
        return task

    def accept_result(self, node, data):
        self.project.store_data(node.task_id, data)
        self._tasks_pool.remove(node.task_id)


class ResultsComparatorController(Controller):
    def __init__(self, *args, **kwargs):
        super(ResultsComparatorController, self).__init__(*args, **kwargs)
        self._comparison_nodes = kwargs['comparison_nodes']
        self._tasks_pool = set()

    def get_task(self, node):
        if not self.project.depleted:
            try:
                task = next(self.project)
            except StopIteration:
                # at this point, project.depleted is expected
                # to become 'True'
                pass

        if self.project.depleted:
            try:
                tp_id = self._tasks_pool.pop()
                task = self.project[tp_id]
            except KeyError:
                # project depleted and nothing in the pool,
                # looks like the application has completed.
                raise AppCompletedError(self.app_name)

        if node.id in self.storage[task.id]:
            raise StopIteration('Node has already completed task #{}'
                                .format(task.id))

        node.task_id = task.id
        self._tasks_pool.add(task.id)
        return task

    def accept_result(self, node, data):
        task_id = node.task_id
        # 'results' computed for the task by various nodes
        results = self.storage[task_id]
        if len(results) == self._comparison_nodes - 1:
            if self._results_are_equal(data, results):
                del self.storage[task_id]
                self._tasks_pool.remove(task_id)
                self._add_result(task_id, data)
            else:
                # Something is wrong with either current result or any result
                # which was received previously. At this point we discard all
                # results associated with task_id and task_id remains in
                # tasks_pool.
                del self.storage[task_id]
            node.task_id = None
        else:
            self.storage.add(node.id, task_id, data)

    def _results_are_equal(self, r0, res):
        for node_id, res in res.iteritems():
            if r0 != res:
                return False
        return True

    def _add_result(self, task_id, data):
        self.project.store_result(task_id, data)
        # check if application has collected all the results
        # and can switch to the "COMPLETED" state
        if self.project.completed:
            self.state = COMPLETED
            self.storage.clear()
