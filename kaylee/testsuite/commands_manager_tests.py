# -*- coding: utf-8 -*-
from kaylee.testsuite import KayleeTest, load_tests
from kaylee.conf.manager import CommandsManager

class KayleeCommandsManagerTests(KayleeTest):
    def test_manager(self):
        pass

kaylee_suite = load_tests([KayleeCommandsManagerTests])
