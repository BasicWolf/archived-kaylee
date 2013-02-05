# -*- coding: utf-8 -*-
from kaylee.testsuite import KayleeTest, load_tests
from kaylee.conf.manager import CommandsManager, BaseCommand
from kaylee.util import nostderr

class KayleeCommandsManagerTests(KayleeTest):

    class SimpleCommand(BaseCommand):
        name = 'simple'

    class CommandWithBlankName(BaseCommand):
        name = ''


    def test_init(self):
        manager = CommandsManager()

    def test_add_command(self):
        manager = CommandsManager()
        self.assertRaises(ValueError,
                          manager.add_command,
                          self.CommandWithBlankName)

    def test_start_project(self):
        manager = CommandsManager()
        with nostderr():
            self.assertRaises(SystemExit, manager.parse, ['startproject'])
            self.assertRaises(SystemExit, manager.parse, 'startproject')

        manager.parse('startproject pi_calculator')
        

kaylee_suite = load_tests([KayleeCommandsManagerTests])
