# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod, abstractproperty
from datetime import datetime

from .node import Node
from .errors import AppFinishedError

ACTIVE = 0x2
FINISHED = 0x4

class Controller(object):
    __metaclass__ = ABCMeta
    def __init__(self, id, app_name, project, results_storage,
                 app_results_storage, *args, **kwargs):
        self.id = id
        self.app_name = app_name
        self.project = project
        self.results = results_storage
        self.app_results = app_results_storage
        self.state = ACTIVE

    def subscribe(self, node):
        """Subscribe Node for bound project"""
        if self.state != FINISHED:
            node.controller = self
            node.subscription_timestamp = datetime.now()
            return self.project.nodes_config
        else:
            raise AppFinishedError(self.app_name)

    @abstractmethod
    def get_task(self, node):
        """ """

    @abstractmethod
    def accept_result(self, node, results):
        """ """


class ResultsComparatorController(Controller):
    def __init__(self, *args, **kwargs):
        super(ResultsComparatorController, self).__init__(*args, **kwargs)
        self._comparison_nodes = kwargs['comparison_nodes']
        self._tasks_pool = set()
        self._no_more_new_tasks = False

    def get_task(self, node):
        if self.state == FINISHED:
            raise AppFinishedError(self.app_name)
        try:
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
                task = next(self.project)
        except StopIteration:
            # There will be no more new tasks from the project
            # we can still refer to old tasks via project[task_id]
            # by re-throwing StopIteration() Controller 'tells' dispatcher that
            # there is no need to involve current node in further calculations
            self._no_more_new_tasks = True
            raise StopIteration('Current node is not allowed to participate '
                                'in calculations for "{}" application anymore '
                                'and will be unsubscribed.'
                                .format(self.app_name))
        task_id = task['task']['id']
        node.task_id = task_id
        self._tasks_pool.add(task_id)
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
        if self._no_more_new_tasks == True:
            if len(self._tasks_pool) == 0:
                self._state = FINISHED
                self.results.clear()
                # TODO: think of this part, what should we do here?
                # e.g. should controller have a function that would do
                # something with results?
