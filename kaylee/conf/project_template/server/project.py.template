from kaylee.project import Project, {{ project_mode }}


class {{project_class_name}}(Project):
    mode = {{ project_mode }}

    def __init__(self, *args, **kwargs):
        super({{ project_class_name }}, self).__init__(*args, **kwargs)

        self.client_config.update({

        })

    def next_task(self):
        pass

    def __getitem__(self, task_id):
        return {
            'id' : 'obligatory_task_id_here'
        }

    def normalize_result(self, task_id, result):
        raise InvalidResultError(result, 'the result is invalid')

    def result_stored(self, task_id, result, storage):
        pass
