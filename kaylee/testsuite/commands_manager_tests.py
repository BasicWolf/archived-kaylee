# -*- coding: utf-8 -*-
import os
import sys
import stat
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
    tmpdir = tempfile.mkdtemp(prefix='kl_unit_test__')
    os.chdir(tmpdir)
    return tmpdir


class KayleeCommandsManagerTests(KayleeTest):
    class CommandWithBlankName(BaseCommand):
        #pylint: disable-msg=W0223
        #W0223:  Method 'execute' is abstract in class 'BaseCommand'
        #        but is not overridden (throws NotImplementedError)
        name = ''

    def tearDown(self):
        tmpdir = tempfile.gettempdir()
        for tdir in os.listdir(tmpdir):
            if tdir.startswith('kl_unit_test__'):
                shutil.rmtree(os.path.join(tmpdir, tdir))

    def test_init(self):
        #pylint: disable-msg=R0201
        #R0201: Method could be a function
        AdminCommandsManager()

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

        self.assertTrue(os.stat(_pjoin(tmpdir, 'klenv/klmanage.py')).st_mode
                        & stat.S_IEXEC)
        # test settings contents
        settings_path = _pjoin(tmpdir, 'klenv/settings.py')
        settings = imp.load_source('tsettings', settings_path)
        self.assertEqual(settings.PROJECTS_DIR,
                         _pjoin(tmpdir, 'klenv'))

        # test 'startenv .' case
        tmpdir = tmp_chdir()
        with nostdout():
            manager.parse(['startenv', '.'])
        files_to_validate = [
            'klmanage.py',
            'settings.py',
        ]
        for fpath in files_to_validate:
            full_path = _pjoin(tmpdir, fpath)
            self.assertGreater(os.path.getsize(full_path), 0)


    def test_start_project(self):
        manager = LocalCommandsManager()
        with nostdout():
            self.assertRaises(SystemExit, manager.parse, ['startproject'])
            self.assertRaises(SystemExit, manager.parse,
                              ['startproject', 'ProjectName', '-m', 'x'])
            self.assertRaises(SystemExit, manager.parse,
                              ['startproject', 'ProjectName', '-t', 'abc'])

        # test for invalid project name
        self.assertRaises(ValueError, manager.parse, ['startproject', '@$'])
        self.assertRaises(ValueError, manager.parse,
                          ['startproject', 'Projec Name'])

        # test for generated project contents
        # create a project in a temporary current working dir
        tmpdir = tmp_chdir()

        with nostdout():
            manager.parse(['startproject', 'Monte_Carlo_Pi'])

        files_to_validate = [
            'monte_carlo_pi/client/monte_carlo_pi.js',
            'monte_carlo_pi/__init__.py',
            'monte_carlo_pi/monte_carlo_pi.py',
        ]

        self._validate_content(RES_DIR, tmpdir, files_to_validate)

    def test_start_project_coffee(self):
        manager = LocalCommandsManager()
        tmpdir = tmp_chdir()

        with nostdout():
            manager.parse(['startproject', 'Pi_Calc', '-t', 'coffee'])

        files_to_validate = [
            'pi_calc/client/pi_calc.coffee',
            'pi_calc/__init__.py',
            'pi_calc/pi_calc.py',
        ]

        self._validate_content(RES_DIR, tmpdir, files_to_validate)

    def test_build(self):
        lmanager = LocalCommandsManager()
        env_path = _start_env()
        os.chdir(env_path)

        # copy a test 'pi calc' project to the environment
        res_path = _pjoin(RES_DIR, 'pi_calc')
        dest_path = _pjoin(env_path, 'pi_calc')
        shutil.copytree(res_path, dest_path)

        # test plain is_kaylee_project_directory()
        sys.path.insert(0, env_path)
        from kaylee.manager.commands.build import is_kaylee_project_directory
        self.assertTrue(is_kaylee_project_directory(res_path))
        self.assertFalse(is_kaylee_project_directory('/etc'))
        del sys.path[0]

        with nostdout():
            lmanager.parse(['build'])

        build_path = os.path.join(env_path, '_build')
        self.assertTrue(os.path.exists(build_path), build_path)
        project_files_to_validate = [
            'js/pi_calc.js',
            'css/pi_calc.css',
            'css/other.css',
            'js/somelib.js',
            'js/otherlib.js',
            'data/somedata.dat',
            'data/otherdata',
        ]
        for fname in project_files_to_validate:
            fpath = os.path.join(build_path, 'pi_calc', fname)
            self.assertTrue(os.path.exists(fpath), fpath)

        kaylee_files_to_validate = [
            'js/kaylee.js',
            'js/klworker.js',
            'js/kldebug.js',
            'js/jquery.min.js',
            'css/klconsole.css'
        ]
        for fname in kaylee_files_to_validate:
            fpath = os.path.join(build_path, 'kaylee', fname)
            self.assertTrue(os.path.exists(fpath))

    def test_run(self):
        env_path = _start_env()
        os.chdir(env_path)
        lmanager = LocalCommandsManager()

        with nostdout():
            self.assertRaises(OSError, lmanager.parse, ['run'])


    def _validate_content(self, gtdir, tmpdir, files_to_validate):
        for fpath in files_to_validate:
            with open(_pjoin(tmpdir, fpath)) as f:
                generated_file_contents = f.read()
            with open(_pjoin(gtdir, fpath)) as f:
                ground_truth_file_contents = f.read().rstrip('\n')

            self.assertEqual(generated_file_contents,
                             ground_truth_file_contents)



def _start_env(name='tenv'):
    amanager = AdminCommandsManager()

    tmpdir = tmp_chdir()
    env_path = os.path.abspath(_pjoin(tmpdir, name))

    with nostdout():
        amanager.parse(['startenv', 'tenv'])
    return env_path





kaylee_suite = load_tests([KayleeCommandsManagerTests])
