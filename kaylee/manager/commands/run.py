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
    def execute(opts):
        validate_settings_file()
        validate_build_dir()

        run_dev_server(opts)


def validate_settings_file(opts):
    if not os.path.exists(ns.settings_file):
        raise OSError('Cannot find the settings file "{}"'
                      .format(opts.settings_file))


def validate_build_dir(opts):
    if not os.path.exists(opts.build_dir):
        raise OSError (
            'Cannot find build directory "{}". \n'
            'Have you forgotten building the environment? \n'
            'If not, please specify with -b or --build-dir.'
            .format(ns.build_dir))


def run_dev_server(opts):
    print('Launching Kaylee development/testing server...')
    run(ns.settings_file, ns.build_dir)
