from kaylee import Project, Controller
from kaylee.project import AUTO_PROJECT_MODE
from kaylee.storage import TemporalStorage, PermanentStorage


class AutoTestProject(Project):
    mode = AUTO_PROJECT_MODE
    RESULT_KEY = 'dres'

    def __init__(self, *args, **kwargs):
        super(AutoTestProject, self).__init__(script = '', *args, **kwargs)
        self.task_id = 0
        self.tasks_count = kwargs.get('tasks_count', 10)
        self.client_config.update({'dummy_key' : 'dummy_value'})

    def __getitem__(self, task_id):
        return {
            'id' : task_id,
        }

    def next_task(self):
        if self.task_id < tasks_count:
            self.task_id += 1
            return self[task_id]
        else:
            return None

    def normalize_result(self, task_id, result):
        try:
            res = int(result[self.RESULT_KEY])
            return res
        except KeyError, ValueError:
            raise InvalidResultError(result, 'The result is wrong.')

    def result_stored(self, task_id, result, storage):
        if len(storage) == 10:
            self.completed = True


class DummyController(Controller):
    def __init__(self, *args, **kwargs):
        super(DummyController, self).__init__(*args, **kwargs)

    def get_task(self, node):
        return next(self.project)

    def accept_result(self, node, data):
        pass

    @staticmethod
    def new_test_instance():
        return DummyController('dummy_app',
                               AutoTestProject(),
                               DummyPermanentStorage(),
                               DummyTemporalStorage())


class DummyTemporalStorage(TemporalStorage):
    def add(self, node_id, task_id, result):
        pass

    def remove(self, node_id, task_id):
        pass

    def clear(self):
        pass

    def keys(self):
        pass

    def values(self):
        pass

    def __len__(self):
        pass

    def __getitem__(self, task_id):
        pass

    def __delitem__(self, task_id):
        pass

    def __contains__(self, task_id):
        pass


class DummyPermanentStorage(PermanentStorage):
    def add(self, task_id, result):
        pass

    def keys(self):
        pass

    def values(self):
        pass

    def __len__(self):
        pass

    def __getitem__(self, task_id):
        pass

    def __contains__(self, task_id):
        pass

    def __iter__(self):
        pass
