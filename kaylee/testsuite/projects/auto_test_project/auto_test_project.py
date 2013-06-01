from kaylee import Project
from kaylee.project import AUTO_PROJECT_MODE
from kaylee.errors import InvalidResultError

class AutoTestProject(Project):
    RESULT_KEY = 'res'
    TASKS_COUNT = 10

    def __init__(self, *args, **kwargs):
        super(AutoTestProject, self).__init__(script_url='',
                                              mode=AUTO_PROJECT_MODE,
                                              *args,
                                              **kwargs)
        self.task_id = 0
        self.tasks_count = kwargs.get('tasks_count', self.TASKS_COUNT)
        self.client_config.update({'test_key' : 'test_value'})

    def __getitem__(self, task_id):
        return {
            'id': str(task_id),
        }

    def next_task(self):
        if self.task_id < self.tasks_count:
            self.task_id += 1
            return self[self.task_id]
        else:
            return None

    def normalize_result(self, task_id, result):
        try:
            res = int(result[self.RESULT_KEY])
            return res
        except (KeyError, ValueError):
            raise InvalidResultError(result, 'The result is wrong.')

    #pylint: disable-msg=W0613
    #W0613: Unused argument 'result'
    def result_stored(self, task_id, result, storage):
        if len(storage) == self.TASKS_COUNT:
            self.completed = True
