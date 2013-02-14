# -*- coding: utf-8 -*-
import os
import tempfile
import shutil

from kaylee.testsuite import KayleeTest, load_tests
from kaylee.manager import (AdminCommandsManager, LocalCommandsManager,
                            BaseCommand)
from kaylee.util import nostdout

CURRENT_DIR = os.path.dirname(__file__)
RES_DIR = os.path.join(CURRENT_DIR, 'command_manager_tests_resources/')

def tmp_chdir():
    tmpdir = tempfile.mkdtemp(prefix='kl_')
    os.chdir(tmpdir)
    return tmpdir


class KayleeCommandsManagerTests(KayleeTest):
    class SimpleCommand(BaseCommand):
        name = 'simple'

    class CommandWithBlankName(BaseCommand):
        name = ''

    def test_init(self):
        manager = AdminCommandsManager()

    def test_add_command(self):
        manager = LocalCommandsManager()
        self.assertRaises(ValueError,
                          manager.add_command,
                          self.CommandWithBlankName)

    def test_local_manager(self):
        manager = LocalCommandsManager()
        with nostdout():
            self.assertRaises(SystemExit, manager.parse, ['bad_command_name'])

    def test_admin_manager(self):
        manager = AdminCommandsManager()
        with nostdout():
            self.assertRaises(SystemExit, manager.parse, ['bad_command_name'])

    def test_start_env(self):
        manager = AdminCommandsManager()

        with nostdout():
            self.assertRaises(SystemExit, manager.parse, ['startenv'])

        tmpdir = tmp_chdir()
        with nostdout():
            manager.parse(['startenv', 'klenv'])

        files_to_validate = [
            'klenv/klmanage.py',
            'klenv/settings.py',
        ]

        for fpath in files_to_validate:
            full_path = os.path.join(tmpdir, fpath)
            self.assertGreater(os.path.getsize(full_path), 0)

    def test_start_project(self):
        manager = LocalCommandsManager()
        with nostdout():
            self.assertRaises(SystemExit, manager.parse, ['startproject'])
            self.assertRaises(SystemExit, manager.parse,
                              ['startproject', 'PiCalc', '-m', 'x'])

        # test for invalid project name
        self.assertRaises(ValueError, manager.parse, ['startproject', '@$'])
        self.assertRaises(ValueError, manager.parse,
                          ['startproject', 'Pi Calc'])

        # test for generated project contents
        # create a project in a temporary current working dir
        tmpdir = tmp_chdir()

        with nostdout():
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
                ground_truth_file_contents = f.read().rstrip('\n')

            self.assertEqual(generated_file_contents,
                             ground_truth_file_contents)

        shutil.rmtree(tmpdir)




kaylee_suite = load_tests([KayleeCommandsManagerTests])
