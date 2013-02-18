from __future__ import print_function
import os
import sys
import re
import argparse
import shutil
from jinja2 import Template
from kaylee.server import run
from kaylee.manager import LocalCommand

import logging
log = logging.getLogger(__name__)


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
            print('Cannot find settings file "{}"'.format(ns.settings_file),
                  file=sys.stderr)
            sys.exit(2)

        if not os.path.exists(ns.build_dir):
            print('Cannot find build directory "{}". Have you forgotten '
                  'building the environment?'.format(ns.build_dir),
                  file=sys.stderr)
            sys.exit(2)

        run(ns.settings_file, ns.build_dir)
