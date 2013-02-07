# -*- coding: utf-8 -*-
import os
import tempfile
import shutil

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

        # create a project in a temporary current working dir
        tmpdir = tempfile.mkdtemp(prefix='kl_')
        os.chdir(tmpdir)

        self.assertRaises(ValueError, manager.parse, ['startproject', '@$'])

        PROJECT_NAME = 'Pi_Calc'
        manager.parse(['startproject', PROJECT_NAME])

        with open(os.path.join(tmpdir,
                               PROJECT_NAME,
                               'client/{}'.format(PROJECT_NAME))) as f:
            file_contents = f.read()
        self.assertEqual(file_contents, )
        """from .pi_calc import PI_Calc"""
        shutil.rmtree(tmpdir)



kaylee_suite = load_tests([KayleeCommandsManagerTests])
