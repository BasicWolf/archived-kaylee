from kaylee import Controller
from kaylee.errors import StopApplication

class SimpleController(Controller):
    auto_filter = True

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
                raise StopApplication(self.app_name)

        node.task_id = task.id
        self._tasks_pool.add(task.id)
        return task

    def accept_result(self, node, data):
        self.project.store_result(node.task_id, data)
        self._tasks_pool.remove(node.task_id)
        if self.project.completed:
            self.completed = True


class ResultsComparatorController(Controller):
    auto_filter = True

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
                raise StopApplication(self.app_name)

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
            self.completed = True
            self.storage.clear()

