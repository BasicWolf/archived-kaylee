from __future__ import print_function
import os
import sys
import imp
from kaylee import Project
from kaylee.manager import LocalCommand
from kaylee.loader import find_packages
from kaylee.util import fwalk


handlers = [

    ]

class BuildCommand(LocalCommand):
    name = 'build'
    help = 'Build Kaylee environment'

    args = {
        ('-s', '--settings-file') : dict(default='settings.py'),
        ('-b', '--build-dir') : dict(default='_build')
    }

    filetype_handlers = [
        BuildCommand.coffee_handler,
        BuildCommand.script_handler,
        BuildCommand.stylesheet_handler,
        BuildCommand.data_handler,
    ]

    @staticmethod
    def execute(ns):
        print('Building Kaylee environment...')

        if not os.path.exists(ns.settings_file):
            print('Cannot find the settings file "{}"'.format(
                ns.settings_file), file=sys.stderr)
            sys.exit(2)

        settings = imp.load_source(ns.settings_file)

        try:
            os.mkdir(ns.build_dir)
        except OSError as e:
            raise OSError('Failed to create build directory {}: {}'
                          .format(ns.build_dir, e))

        for pkg_dir in find_packages(settings.PROJECTS_DIR):
            client_dir = os.path.join(pkg_dir, 'client')
            if not os.path.isdir(client_dir):
                break

            for fpath in fwalk(client_dir):
                for handler in self.file_handlers:
                    if handler(fpath, ns) == True:
                        break

        # 3. Build the client as follows:
        #    os.walk() the client dir
        #    for each coffee file - compile it
        #    move every file to corresponding directory
        #    e.g. '.js' to 'js', '.css' to 'css', '.png/.jpg/etc.' to 'img'
        #       the rest - move to 'data'. Make sure that these options are
        #       configurable through command-line.

    @staticmethod
    def coffee_handler(fpath, opts):
        lstrun = ['coffee', ]
        pass
