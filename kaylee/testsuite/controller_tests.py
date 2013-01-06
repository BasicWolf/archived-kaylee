# -*- coding: utf-8 -*-
from kaylee.testsuite import (KayleeTest, load_tests, TestTemporalStorage,
                              TestPermanentStorage)
from kaylee.testsuite.projects.dummy_project import AutoTestProject
from kaylee.contrib.controllers import SimpleController


class SimpleControllerTests(KayleeTest):
    def setUp(self):

        pass

    def test_init(self):
        pass


kaylee_suite = load_tests([SimpleControllerTests,])
