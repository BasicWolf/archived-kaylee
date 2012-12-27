from kaylee.project import Project

class NonAbstractProject(Project):
    def __init__(self, *args, **kwargs):
        pass

    def __getitem__(self, task_id):
        pass

    def next_task(self):
        pass

    def normalize_result(self, task_id, result):
        pass

    def result_stored(self, task_id, result, storage):
        pass
