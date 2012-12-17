# -*- coding: utf-8 -*-
from kaylee.controller import Controller, NO_SOLUTION, NOT_SOLVED
from kaylee.errors import ApplicationCompletedError, NodeRequestRejectedError

class SimpleController(Controller):
    """
    This is a very basic controller which serves the tasks by
    Node requests and passes the accepted results directly to the project.
    Its ``completed`` indicator is set to ``True`` the moment the bound
    project is completed. The controller doesn't use temporal storage.
    """
    def __init__(self, *args, **kwargs):
        super(SimpleController, self).__init__(*args, **kwargs)
        self._tasks_pool = set()
        self._project_depleted = False

    def get_task(self, node):
        task = self.project.next_task()
        if task is None:
            try:
                tp_id = self._tasks_pool.pop()
                task = self.project[tp_id]
            except KeyError:
                # project depleted and nothing in the pool,
                # looks like the application is completed.
                self.completed = True
                raise ApplicationCompletedError(self)

        task_id = task['id']
        node.task_id = task_id
        self._tasks_pool.add(task_id)
        return task

    def accept_result(self, node, result):
        if result == NO_SOLUTION:
            self._tasks_pool.remove(node.task_id)
            return
        elif result == NOT_SOLVED:
            return

        norm_result = self.project.normalize_result(node.task_id, result)
        self.store_result(node.task_id, norm_result)
        self._tasks_pool.remove(node.task_id)
        if self.project.completed:
            self.completed = True



class ResultsComparatorController(Controller):
    """
    This controller is a simple implementation of the "trust no one" idea.
    The intermediate results are collected in the temporal storage until
    their number reaches a user-defined limit. Then the results are pairly
    compared and only if they all match among themselves, a single result
    is stored inside the permanent storage. The results are discarded if they
    don't match and the task is pushed back to the "unsolved tasks" pool.

    :param results_count_threshold: The amount of task results to be collected
                                    before running the comparison routine.
    """
    def __init__(self, *args, **kwargs):
        super(ResultsComparatorController, self).__init__(*args, **kwargs)
        self._results_count_threshold = kwargs['results_count_threshold']
        self._tasks_pool = set()

    def get_task(self, node):
        task = self.project.next_task()
        if task is None:
            try:
                tp_id = self._tasks_pool.pop()
                task = self.project[tp_id]
            except KeyError:
                # project depleted and nothing in the pool,
                # looks like the application has completed.
                self.completed = True
                raise ApplicationCompletedError(self)

        task_id = task['id']
        node.task_id = task_id
        self._tasks_pool.add(task_id)

        if node.id in self.temporal_storage[task_id]:
            raise NodeRequestRejectedError('The result of this task has been '
                                           'already accepted.')
        return task

    def accept_result(self, node, result):
        if result == NOT_SOLVED:
            return

        task_id = node.task_id

        if result == NO_SOLUTION:
            norm_result = result
        else:
            norm_result = self.project.normalize_result(task_id, result)

        # 'results' computed for the task by various nodes
        tmp_results = self.temporal_storage[task_id]
        if len(tmp_results) == self._results_count_threshold - 1:
            if self._results_are_equal(norm_result, tmp_results):
                del self.temporal_storage[task_id]
                self._tasks_pool.remove(task_id)
                if result != NO_SOLUTION:
                    self.store_result(task_id, norm_result)
            else:
                # Something is wrong with either current result or any result
                # which was received previously. At this point we discard all
                # results associated with task_id and task_id remains in
                # tasks_pool (if the result is not NO_SOLUTION)
                del self.temporal_storage[task_id]
                if result == NO_SOLUTION:
                    self._tasks_pool.remove(task_id)
            node.task_id = None
        else:
            self.temporal_storage.add(node.id, task_id, norm_result)

    @staticmethod
    def _results_are_equal(r0, res):
        #pylint: disable-msg=W0612
        #W0612: Unused variable 'node_id'
        ###
        for node_id, res in res.iteritems():
            if r0 != res:
                return False
        return True

    def store_result(self, task_id, result):
        super(ResultsComparatorController, self).store_result(task_id, result)
        if self.project.completed:
            self.completed = True
            self.temporal_storage.clear()
