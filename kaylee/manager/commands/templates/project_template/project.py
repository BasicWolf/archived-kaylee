from kaylee.project import Project, {{ project_mode }}
from kaylee.errors import InvalidResultError

class {{project_class_name}}(Project):
    mode = {{ project_mode }}

    def __init__(self, *args, **kwargs):
        super({{ project_class_name }}, self).__init__(*args, **kwargs)

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
