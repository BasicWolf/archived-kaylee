from kaylee.project import Project

from kaylee.contrib.storages import (MemoryTemporalStorage,
                                     MemoryPermanentStorage)
from kaylee.contrib.controllers import SimpleController


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


class TestTemporalStorage(MemoryTemporalStorage):
    pass

class TestPermanentStorage(MemoryPermanentStorage):
    pass

class TestController(SimpleController):

    @staticmethod
    def new_test_instance(project_object=None, app_name='test_app'):
        # Load autoproject from testsuite in order to be able to
        # completely initialize a test controller with all necessary
        # attributes.
        if project_object is None:
            from kaylee.testsuite.projects.test_auto_project \
                import AutoTestProject
            project_object = AutoTestProject()

        return TestController(app_name,
                              project_object,
                              TestPermanentStorage(),
                              TestTemporalStorage())
