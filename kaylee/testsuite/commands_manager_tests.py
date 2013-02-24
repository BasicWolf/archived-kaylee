# -*- coding: utf-8 -*-
import os
import tempfile
import shutil
import imp

from kaylee.testsuite import KayleeTest, load_tests
from kaylee.manager import (AdminCommandsManager, LocalCommandsManager,
                            BaseCommand)
from kaylee.util import nostdout

_pjoin = os.path.join

CURRENT_DIR = os.path.dirname(__file__)
RES_DIR = _pjoin(CURRENT_DIR, 'command_manager_tests_resources/')



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

        # test whether files exist
        files_to_validate = [
            'klenv/klmanage.py',
            'klenv/settings.py',
        ]

        for fpath in files_to_validate:
            full_path = _pjoin(tmpdir, fpath)
            self.assertGreater(os.path.getsize(full_path), 0)

        # test settings contents
        settings_path = _pjoin(tmpdir, 'klenv/settings.py')
        settings = imp.load_source('tsettings', settings_path)
        self.assertEqual(settings.PROJECTS_DIR,
                         _pjoin(tmpdir, 'klenv'))


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
            'pi_calc/__init__.py',
            'pi_calc/pi_calc.py',
        ]

        for fpath in files_to_validate:
            with open(_pjoin(tmpdir, fpath)) as f:
                generated_file_contents = f.read()
            with open(_pjoin(RES_DIR, fpath)) as f:
                ground_truth_file_contents = f.read().rstrip('\n')

            self.assertEqual(generated_file_contents,
                             ground_truth_file_contents)

        shutil.rmtree(tmpdir)

    def test_build(self):
        amanager = AdminCommandsManager()
        lmanager = LocalCommandsManager()

        tmpdir = tmp_chdir()

        with nostdout():
            amanager.parse(['startenv', 'tenv'])
            lmanager.parse(['startproject', 'Pi_Calc'])

        # copy a ready test 'pi calc' project to the environment
        shutil.copytree(_pjoin(RES_DIR, 'pi_calc'),
                        _pjoin(tmpdir, 'tenv'))

        files_to_validate = [
            'js/pi_calc.js',
            'css/pi_calc.css',
            'css/other.css'
            'js/somelib.js',
            'js/otherlib.js',
            'data/somelib.dat',
            'data/atheist'
        ]

        with nostdout():
            lmanager.parse(['build'])

        for fname in files_to_validate:
            fpath = os.path.join(tmpdir, '_build', fname)
            self.assertTrue(os.path.exists(fpath))

        shutil.rmtree(tmpdir)



    def test_run(self):
        manager = LocalCommandsManager()
        with nostdout():
            self.assertRaises(SystemExit, manager.parse, ['run'])



kaylee_suite = load_tests([KayleeCommandsManagerTests])
