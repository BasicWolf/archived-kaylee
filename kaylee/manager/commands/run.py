from __future__ import print_function
import os
import sys
from kaylee.server import run
from kaylee.manager import LocalCommand


class RunCommand(LocalCommand):
    name = 'run'
    help = 'Runs Kaylee development/testing server'

    args = {
        ('-s', '--settings-file') : dict(default='settings.py'),
        ('-b', '--build-dir') : dict(default='_build')
    }

    @staticmethod
    def execute(ns):
        print('Launching Kaylee development/testing server...')

        if not os.path.exists(ns.settings_file):
            print('Cannot find the settings file "{}"'.format(
                ns.settings_file), file=sys.stderr)
            sys.exit(2)

        if not os.path.exists(ns.build_dir):
            print('Cannot find build directory "{}". \nHave you forgotten '
                  'building the environment? \nIf not, please specify with'
                  ' -b or --build-dir.'.format(ns.build_dir),
                  file=sys.stderr)
            sys.exit(2)

        run(ns.settings_file, ns.build_dir)
