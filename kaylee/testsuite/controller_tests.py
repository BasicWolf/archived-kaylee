# -*- coding: utf-8 -*-
from kaylee.testsuite import (KayleeTest, load_tests, TestTemporalStorage,
                              TestPermanentStorage)
from kaylee.testsuite.projects.auto_test_project import AutoTestProject
from kaylee.contrib.controllers import SimpleController
from abc import ABCMeta

class ControllerTestsBase(KayleeTest):
    __metaclass__ = ABCMeta

    # @abstractmethod
    # def init_cls(self):
    #     pass

    def setUp(self):
        pass

    def test_init(self):
        pass

    def test_get_task(self):
        pass

class SimpleControllerTests(ControllerTestsBase):
    pass

kaylee_suite = load_tests([SimpleControllerTests,])
