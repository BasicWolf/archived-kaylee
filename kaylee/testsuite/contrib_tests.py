# -*- coding: utf-8 -*-
from kaylee.testsuite import KayleeTest, load_tests
from kaylee.testsuite.projects.dummy_project import AutoTestProject
from kaylee.contrib.controllers import SimpleController
from kaylee.contrib.storages import MemoryPermanentStorage


class SimpleControllerTests(KayleeTest):
    def setUp(self):

        pass

    def test_init(self):
        pass


class MemoryPermanentStorageTests(KayleeTest):

    def test_init(self):
        m = MemoryPermanentStorage()
        self.assertEqual(len(m), 0)

    def test_add_one(self):
        m = MemoryPermanentStorage()
        m.add('1', 'r1')

        self.assertEqual(m['1'], ['r1'])
        self.assertEqual(len(m), 1)
        self.assertEqual(list(iter(m)), ['1'])

    def test_add_many(self):
        m = MemoryPermanentStorage()

        COUNT = 100
        for i in range(0, COUNT):
            m.add(str(i), 'r' + str(i))

        self.assertEqual(len(m), COUNT)

        for i in range(0, COUNT):
            self.assertEqual(m[str(i)], ['r' + str(i)])

        keys_set = set(str(i) for i in range(0, COUNT))
        self.assertEqual(set(iter(m)), keys_set)


kaylee_suite = load_tests([SimpleControllerTests,
                           MemoryPermanentStorageTests])
