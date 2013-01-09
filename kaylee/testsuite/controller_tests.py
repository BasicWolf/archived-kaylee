# -*- coding: utf-8 -*-
from kaylee.testsuite import (load_tests, TestTemporalStorage,
                              TestPermanentStorage)
from kaylee.testsuite.projects.auto_test_project import AutoTestProject
from kaylee.contrib.controllers import SimpleController
from kaylee.testsuite.helper import SubclassTestsBase
from abc import ABCMeta, abstractmethod

class ControllerTestsBase(SubclassTestsBase):
    __metaclass__ = ABCMeta

    def setUp(self):
        super(ControllerTestsBase, self).setUp()

    @abstractmethod
    def test_init(self):
        pass

    # def test_get_task(self):
    #     ctr = self.cls_instance()



class SimpleControllerTests(ControllerTestsBase):
    def test_init(self):
        pass

    def cls_instance(self):
        return SimpleController('test_app',
                                AutoTestProject(),
                                TestPermanentStorage())


kaylee_suite = load_tests([SimpleControllerTests,])
