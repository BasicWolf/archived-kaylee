# -*- coding: utf-8 -*-
"""
    kaylee.controller
    ~~~~~~~~~~~~~~~~~

    This module provides classes for Kaylee controllers.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""
import re
from abc import ABCMeta, abstractmethod, abstractproperty
from datetime import datetime

from .node import Node
from .errors import AppFinishedError

#: The Application name regular expression pattern which can be used in
#: e.g. web frameworks' URL dispatchers.
app_name_pattern = r'[a-zA-Z\.\d_-]+'
_app_name_re = re.compile('^{}$'.format(app_name_pattern))

ACTIVE = 0x2
FINISHED = 0x4


def app_finished_guard(f):
    def wrapper(self, *args, **kwargs):
        if self.state == FINISHED:
            raise AppFinishedError(self.app_name)
        return f(self, *args, **kwargs)
    return wrapper

def normalize_result(f):
    def wrapper(self, node, data):
        data = self.project.normalize(data)
        return f(self, node, data)
    return wrapper

class ControllerMeta(ABCMeta):
    _auto_get_task_wrappers = [
        app_finished_guard,
    ]

    _auto_accept_result_wrappers = [
        normalize_result,
    ]

    def __new__(cls, name, bases, dct):
        auto_wrap = dct.get('auto_wrap', True)
        if auto_wrap:
            # Automatically wrap 'get_task' and 'accept_result' method
            # so that the user does not have to worry about the common
            # stuff.
            method = dct['accept_result']
            for wrapper in ControllerMeta._auto_accept_result_wrappers:
                method = wrapper(method)
            dct['accept_result'] = method

            method = dct['get_task']
            for wrapper in ControllerMeta._auto_get_task_wrappers:
                method = wrapper(method)
            dct['get_task'] = method

        return super(ControllerMeta, cls).__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super(ControllerMeta, cls).__init__(name, bases, dct)


class Controller(object):
    __metaclass__ = ControllerMeta
    auto_wrap = True

    def __init__(self, id, app_name, project, results_storage,
                 app_results_storage, *args, **kwargs):
        if _app_name_re.match(app_name) is None:
            raise ValueError('Invalid application name: {}'.format(app_name))
        self.id = id
        self.app_name = app_name
        self.project = project
        self.results = results_storage
        self.app_results = app_results_storage
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
        self._tasks_pool = set()

    def get_task(self, node):
        try:
            if node.task_id is None or node.task_id in self.app_results:
                # try getting a task from the pool
                tp_id = self._tasks_pool.pop()
                task = self.project[tp_id]
            else:
                # repeat the same task
                task = self.project[node.task_id]
        except KeyError:
            # nothing in the pool, get a new task
            task = next(self.project)

        node.task_id = task.id
        self._tasks_pool.add(task.id)
        return task

    def accept_result(self, node, data):
        pass


class ResultsComparatorController(Controller):
    def __init__(self, *args, **kwargs):
        super(ResultsComparatorController, self).__init__(*args, **kwargs)
        self._comparison_nodes = kwargs['comparison_nodes']
        self._tasks_pool = set()

    def get_task(self, node):
        try:
            if node.task_id is None or node.task_id in self.app_results:
                # try getting a task from the pool
                tp_id = self._tasks_pool.pop()
                task = self.project[tp_id]
            elif node.id in self.results[node.task_id]:
                # DO NOT repeat the task, instead send a new task to Node
                task = next(self.project)
            else:
                # repeat the same task
                task = self.project[node.task_id]
        except KeyError:
            # nothing in the pool, get a new task
            task = next(self.project)

        node.task_id = task.id
        self._tasks_pool.add(task.id)
        return task

    def accept_result(self, node, data):
        task_id = node.task_id
        # 'results' computed for the task by various nodes
        results = self.results[task_id]
        if len(results) == self._comparison_nodes - 1:
            if self._results_are_equal(data, results):
                del self.results[task_id]
                self._tasks_pool.remove(task_id)
                self._add_result(task_id, data)
            else:
                # Something is wrong with either current result or any result
                # which was received previously. At this point we discard all
                # results associated with task_id and task_id remains in
                # tasks_pool.
                del self.results[task_id]
            node.task_id = None
        else:
            self.results.add(node.id, task_id, data)

    def _results_are_equal(self, r0, res):
        for node_id, res in res.iteritems():
            if r0 != res:
                return False
        return True

    def _add_result(self, task_id, data):
        self.app_results[task_id] = data
        # check if application has collected all the results
        # and can switch to "FINISHED" state
        if self.project.depleted:
            if len(self._tasks_pool) == 0:
                self.state = FINISHED
                self.results.clear()
                # TODO: think of this part, what should we do here?
                # e.g. should controller have a function that would do
                # something with results?
