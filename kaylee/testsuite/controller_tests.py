# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from kaylee.testsuite import (load_tests, TestPermanentStorage)
from kaylee.testsuite.helper import SubclassTestsBase
from kaylee.testsuite.projects.auto_test_project import AutoTestProject
from kaylee.node import Node, NodeID
from kaylee.contrib.controllers import SimpleController
from kaylee.errors import InvalidResultError



class ControllerTestsBase(SubclassTestsBase):
    """The class contains only basic generic tests that can be applied
    to any controller. Please subclass and extend the tests for thorough
    testing.
    """
    __metaclass__ = ABCMeta

    def setUp(self):
        super(ControllerTestsBase, self).setUp()

    @abstractmethod
    def test_init(self):
        pass

    def test_get_task(self):
        node, ctr = self.make_node_and_controller()
        task = ctr.get_task(node)
        self.assertIsInstance(task, dict)
        self.assertIn('id', task)
        self.assertTrue(len(str(task['id']).strip()) > 0)

        #pylint: disable-msg=W0612
        for i in range(0, self.MANY):
            task = ctr.get_task(node)
            self.assertTrue(task is None or isinstance(task, dict))

    def test_accept_result(self):
        node, ctr = self.make_node_and_controller()
        task = ctr.get_task(node)
        res = { 'res' : task['id'] }
        ctr.accept_result(node, res)
        self.assertRaises(InvalidResultError, ctr.accept_result, node, {})

    def make_node_and_controller(self):
        ctr = self.cls_instance()
        n = Node(NodeID())
        n.subscribe(ctr)
        return n, ctr


class SimpleControllerTests(ControllerTestsBase):
    def test_init(self):
        pass

    def cls_instance(self):
        return SimpleController('test_simple_controller_app',
                                AutoTestProject(),
                                TestPermanentStorage())


kaylee_suite = load_tests([SimpleControllerTests,])
