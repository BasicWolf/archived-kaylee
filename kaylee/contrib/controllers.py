from kaylee.controller import Controller
from kaylee.errors import ApplicationCompletedError, NodeRejectedError

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
                raise ApplicationCompletedError(self.name)

        task_id = task['id']
        node.task_id = task_id
        self._tasks_pool.add(task_id)
        return task

    def accept_result(self, node, data):
        self.store_result(node.task_id, data)
        self._tasks_pool.remove(node.task_id)
        if self.project.completed:
            self.completed = True



class ResultsComparatorController(Controller):
    """
    This controller is a simple implementation of the idea "trust no one".
    The intermediate results are collected in the temporal storage until
    their number reaches a user-defined limit. Then the results are
    compared and only if they match among themselves, a single result
    is passed to the project. The results are discarded if they don't
    match and the calculations for the task starts again.

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
                raise ApplicationCompletedError(self.name)

        task_id = task['id']
        node.task_id = task_id
        self._tasks_pool.add(task_id)

        if node.id in self.temporal_storage[task_id]:
            raise NodeRejectedError()
        return task

    def accept_result(self, node, data):
        task_id = node.task_id
        # 'results' computed for the task by various nodes
        results = self.temporal_storage[task_id]
        if len(results) == self._results_count_threshold - 1:
            if self._results_are_equal(data, results):
                del self.temporal_storage[task_id]
                self._tasks_pool.remove(task_id)
                self.store_result(task_id, data)
            else:
                # Something is wrong with either current result or any result
                # which was received previously. At this point we discard all
                # results associated with task_id and task_id remains in
                # tasks_pool.
                del self.temporal_storage[task_id]
            node.task_id = None
        else:
            self.temporal_storage.add(node.id, task_id, data)

    def _results_are_equal(self, r0, res):
        for node_id, res in res.iteritems():
            if r0 != res:
                return False
        return True


    def store_result(self, task_id, data):
        super(ResultsComparatorController, self).store_result(task_id, data)
        if self.project.completed:
            self.completed = True
            self.temporal_storage.clear()
