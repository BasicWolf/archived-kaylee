# -*- coding: utf-8 -*-
import os
import tempfile
import shutil

from kaylee.testsuite import KayleeTest, load_tests
from kaylee.conf.manager import CommandsManager, BaseCommand
from kaylee.util import nostderr

CURRENT_DIR = os.path.dirname(__file__)
RES_DIR = os.path.join(CURRENT_DIR, 'command_manager_tests_resources/')

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

        # test for invalid project name
        self.assertRaises(ValueError, manager.parse, ['startproject', '@$'])
        self.assertRaises(ValueError, manager.parse, ['startproject', 'Pi Calc'])

        # test for generated project contents
        # create a project in a temporary current working dir
        tmpdir = tempfile.mkdtemp(prefix='kl_')
        os.chdir(tmpdir)

        manager.parse(['startproject', 'Pi_Calc'])

        files_to_validate = [
            'pi_calc/client/pi_calc.coffee',
            'pi_calc/server/__init__.py',
            'pi_calc/server/pi_calc.py',
        ]

        for fpath in files_to_validate:
            with open(os.path.join(tmpdir, fpath)) as f:
                generated_file_contents = f.read()
            with open(os.path.join(RES_DIR, fpath)) as f:
                ground_truth_file_contents = f.read()

            self.assertEqual(generated_file_contents,
                             ground_truth_file_contents)

        shutil.rmtree(tmpdir)



kaylee_suite = load_tests([KayleeCommandsManagerTests])
