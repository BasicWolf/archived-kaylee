from kaylee import Project
from kaylee.project import AUTO_PROJECT_MODE

class AutoTestProject(Project):
    mode = AUTO_PROJECT_MODE
    RESULT_KEY = 'dres'

    def __init__(self, *args, **kwargs):
        super(AutoTestProject, self).__init__(script = '', *args, **kwargs)
        self.task_id = 0
        self.tasks_count = kwargs.get('tasks_count', 10)
        self.client_config.update({'test_key' : 'test_value'})

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
