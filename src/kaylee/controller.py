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
from collections import deque

from .node import Node
from .util import AutoWrapperABCMeta
from .errors import AppFinishedError

#: The Application name regular expression pattern which can be used in
#: e.g. web frameworks' URL dispatchers.
app_name_pattern = r'[a-zA-Z\.\d_-]+'
_app_name_re = re.compile('^{}$'.format(app_name_pattern))

ACTIVE = 0x2
FINISHED = 0x4


def app_finished_guard(f):
    def wrapper(obj, *args, **kwargs):
        if obj.state == FINISHED:
            raise AppFinishedError(obj.app_name)
        return f(obj, *args, **kwargs)
    return wrapper

def normalize_result(f):
    def wrapper(self, node, data):
        data = self.project.normalize(data)
        return f(self, node, data)
    return wrapper

class ControllerMeta(AutoWrapperABCMeta):
    _wrappers = {
        'get_task' : [
            app_finished_guard,
            ],
        'accept_result' : [
            normalize_result,
            ]
        }


class Controller(object):
    __metaclass__ = ControllerMeta
    auto_wrap = True

    def __init__(self, id, app_name, project, tmp_storage,
                 app_storage, *args, **kwargs):
        if _app_name_re.match(app_name) is None:
            raise ValueError('Invalid application name: {}'.format(app_name))
        self.id = id
        self.app_name = app_name
        self.project = project
        self.tmp_storage = tmp_storage
        self.app_storage = app_storage
        self.state = ACTIVE

    @app_finished_guard
    def subscribe(self, node):
        """Subscribe Node for bound project"""
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
        :param data: JSON-parsed data (python dictionary or list)
        """


class SimpleController(Controller):
    def __init__(self, *args, **kwargs):
        super(SimpleController, self).__init__(*args, **kwargs)
        self._tasks_queue = deque()

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
                tp_id = self._tasks_queue.pop()
                task = self.project[tp_id]
            except KeyError:
                # project depleted and nothing in the pool,
                # looks like the application has finished.
                raise StopIteration

        node.task_id = task.id
        self._tasks_pool.add(task.id)
        return task

    def accept_result(self, node, data):
        task_id = node.task_id
        self.app_storage[task_id] = data


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
                # looks like the application has finished.
                raise StopIteration

        if node.id in self.tmp_storage[task.id]:
            raise StopIteration('Node has already completed task #{}'
                                .format(task.id))

        node.task_id = task.id
        self._tasks_pool.add(task.id)
        return task

    def accept_result(self, node, data):
        task_id = node.task_id
        # 'results' computed for the task by various nodes
        results = self.tmp_storage[task_id]
        if len(results) == self._comparison_nodes - 1:
            if self._results_are_equal(data, results):
                del self.tmp_storage[task_id]
                self._tasks_pool.remove(task_id)
                self._add_result(task_id, data)
            else:
                # Something is wrong with either current result or any result
                # which was received previously. At this point we discard all
                # results associated with task_id and task_id remains in
                # tasks_pool.
                del self.tmp_storage[task_id]
            node.task_id = None
        else:
            self.tmp_storage.add(node.id, task_id, data)

    def _results_are_equal(self, r0, res):
        for node_id, res in res.iteritems():
            if r0 != res:
                return False
        return True

    def _add_result(self, task_id, data):
        self.app_storage[task_id] = data
        # check if application has collected all the results
        # and can switch to "FINISHED" state
        if self.project.depleted:
            if len(self._tasks_pool) == 0:
                self.state = FINISHED
                self.tmp_storage.clear()
                # TODO: think of this part, what should we do here?
                # e.g. should controller have a function that would do
                # something with results?
