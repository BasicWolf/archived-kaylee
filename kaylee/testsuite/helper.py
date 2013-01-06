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


TestTemporalStorage = MemoryTemporalStorage
TestPermanentStorage = MemoryPermanentStorage
TestController = SimpleController
