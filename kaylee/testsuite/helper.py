import unittest
from kaylee.project import Project
from kaylee.contrib.storages import (MemoryTemporalStorage,
                                     MemoryPermanentStorage)
from kaylee.contrib.controllers import SimpleController
from abc import ABCMeta, abstractmethod


class KayleeTest(unittest.TestCase):
    """Base class for all Kaylee tests."""

class SubclassTestsBase(KayleeTest):
    """The base class for (sub)classes, e.g. controllers, storages etc.
    tests. The idea that Kaylee provides basic tests, which can then be
    subclassed and extentended by class-specific tests"""
    SOME = 11
    MANY = SOME ** 2

    __metaclass__ = ABCMeta

    def setUp(self):
        self.cls = self.cls_instance().__class__

    #pylint: disable-msg=R0201
    #R0201: Method could be a function
    @abstractmethod
    def cls_instance(self):
        """Returns an instance of """
        return None


class NonAbstractProject(Project):
    def __init__(self, *args, **kwargs):
        super(NonAbstractProject, self).__init__(*args, **kwargs)

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
            from kaylee.testsuite.projects.auto_test_project \
                import AutoTestProject
            project_object = AutoTestProject()

        return TestController(app_name,
                              project_object,
                              TestPermanentStorage(),
                              TestTemporalStorage())
