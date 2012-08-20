from kaylee import Project, Controller

class DummyProject(Project):
    def __init__(self, *args, **kwargs):
        super(DummyProject, self).__init__(script = '', *args, **kwargs)
        self.x = 0
        self.client_config = { 'dummy_key' : 'dummy_value' }

    def __next__(self):
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
        self.results.add(node.id, node.task_id, data)
