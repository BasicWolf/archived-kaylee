from kaylee import Project, Controller
from kaylee.project import AUTO_PROJECT_MODE
from kaylee.storage import TemporalStorage, PermanentStorage

class DummyProject(Project):
    mode = AUTO_PROJECT_MODE

    def __init__(self, *args, **kwargs):
        super(DummyProject, self).__init__(script = '', *args, **kwargs)
        self.x = 0
        self.client_config = { 'dummy_key' : 'dummy_value' }

    def normalize_result(self, task_id, result):
        return result

    def next_task(self):
        self.x += 1
        return self.x

    def __getitem__(self, val):
        return val


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
                               DummyProject(),
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
