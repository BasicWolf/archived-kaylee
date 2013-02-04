# -*- coding: utf-8 -*-
from kaylee.testsuite import KayleeTest, load_tests
from kaylee.conf.manager import CommandsManager, BaseCommand

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

        


kaylee_suite = load_tests([KayleeCommandsManagerTests])
