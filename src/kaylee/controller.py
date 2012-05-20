# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from datetime import datetime

from .errors import KayleeError
from .node import Node

class Controller(object):
    __metaclass__ = ABCMeta
    def __init__(self, id, app_name, project, results_storage,
                 app_results_storage, *args, **kwargs):
        self.id = id
        self.app_name = app_name
        self.project = project
        self.results = results_storage
        self.app_results = app_results_storage

    def subscribe(self, node):
        """Subscribe Node for bound project"""
        node.controller = self
        node.subscription_timestamp = datetime.now()
        return self.project.nodes_config

    @abstractmethod
    def get_task(self, node):
        """ """

    @abstractmethod
    def accept_results(self, node, task_id, results):
        """ """


class ResultsComparatorController(Controller):
    def __init__(self, *args, **kwargs):
        super(ResultsComparatorController, self).__init__(*args, **kwargs)
        self._comparison_nodes = kwargs['comparison_nodes']
        self._tasks_pool = set()

    def get_task(self, node):
        try:
            if node.task_id is None or node.task_id in self.app_results:
                # try getting a task from the pool
                tp_id = _tasks_pool.pop()
                task = self.project[tp_id]
            else:
                # repeat the same task
                task = project[node.task_id]
        except KeyError:
                task = next(self.project)
        _tasks_pool.add(task['task']['id'])

    def accept_results(self, node, task_id, data):
        # 'results' computed for the task by various nodes
        results = self.results[task_id]
        if len(results) == self._comparison_nodes - 1:
            if self._results_are_equal(data, results):
                self.app_results.add(task_id, data)
                del self._results[task_id]
                self._tasks_pool.remove(task_id)
            else:
                # Something is wrong with either current result or any result
                # which was received previously. At this point we discard all
                # results associated with task_id and task_id remains in
                # tasks_pool.
                del self._results[task_id]
        else:
            self.results.add(node_id, task_id, data)

    def _results_are_equal(self, r0, res):
        for r in res.iteritems():
            if r0 != res:
                return False
        return True

