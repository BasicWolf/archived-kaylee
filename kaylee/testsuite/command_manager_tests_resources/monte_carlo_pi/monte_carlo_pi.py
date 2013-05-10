from kaylee.project import Project, AUTO_PROJECT_MODE
from kaylee.errors import InvalidResultError

class Monte_Carlo_Pi(Project):
    mode = AUTO_PROJECT_MODE

    def __init__(self, *args, **kwargs):
        super(Monte_Carlo_Pi, self).__init__(*args, **kwargs)

        self.client_config.update({

        })

    def __getitem__(self, task_id):
        return {
            'id' : 'obligatory_task_id_here'
        }

    def next_task(self):
        pass

    def normalize_result(self, task_id, result):
        raise InvalidResultError(result, 'The result is invalid.')

    def result_stored(self, task_id, result, storage):
        pass
