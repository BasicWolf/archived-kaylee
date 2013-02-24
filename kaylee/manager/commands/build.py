from __future__ import print_function
import os
import sys
import imp
import subprocess
import shutil
from kaylee import Project
from kaylee.manager import LocalCommand
from kaylee.loader import find_packages
from kaylee.util import ensure_dir


def coffee_handler(fpath, cmd_opts):
    if not fpath.endswith('.coffee'):
        return False

    args = ['coffee', '--bare', '-c', fpath]
    print(' '.join(args))
    proc = subprocess.Popen(args,
                            close_fds=True,
                            stdin=subprocess.PIPE,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE)
    stdoutdata, stderrdata = proc.communicate()
    if stderrdata is not '':
        raise Exception('Error compiling .coffee script:\n{}'
                        .format(stderrdata))

    dest_dir = os.path.join(cmd_opts.dest_dir, 'js')
    ensure_dir(dest_dir)
    outpath = fpath.rstrip('.coffee') + '.js'
    shutil.move(outpath, dest_dir)
    return True


def script_handler(fpath, cmd_opts):
    if not fpath.endswith('.js'):
        return False

    dest_dir = os.path.join(cmd_opts.dest_dir, 'js')
    ensure_dir(dest_dir)
    shutil.copy(fpath, dest_dir)
    return True


def stylesheet_handler(fpath, cmd_opts):
    if not fpath.endswith('.css'):
        return False

    dest_dir = os.path.join(cmd_opts.dest_dir, 'css')
    ensure_dir(dest_dir)
    shutil.copy(fpath, dest_dir)
    return True


def data_handler(fpath, cmd_opts):
    dest_dir = os.path.join(cmd_opts.dest_dir, 'data')
    ensure_dir(dest_dir)
    shutil.copy(fpath, dest_dir)
    return True


class BuildCommand(LocalCommand):
    name = 'build'
    help = 'Build Kaylee environment'

    args = {
        ('-s', '--settings-file') : dict(default='settings.py'),
        ('-b', '--build-dir') : dict(default='_build')
    }

    @staticmethod
    def execute(ns):
        print('Building Kaylee environment...')

        if not os.path.exists(ns.settings_file):
            print('Cannot find the settings file "{}"'.format(
                ns.settings_file), file=sys.stderr)
            sys.exit(2)

        settings = imp.load_source('settings', ns.settings_file)

        try:
            if not os.path.exists(ns.build_dir):
                os.mkdir(ns.build_dir)
        except OSError as e:
            raise OSError('Failed to create build directory {}: {}'
                          .format(ns.build_dir, e))

        filetype_handlers = [
            coffee_handler,
            script_handler,
            stylesheet_handler,
            data_handler,
        ]

        # os.walk for files with by-extension sorting
        def _fwalk(path):
            sort_key = lambda fname: fname.rsplit()[-1]
            for root, dirs, files in os.walk(path):
                for fname in sorted(files, key=sort_key):
                    yield os.path.join(root, fname)

        for pkg_dir in find_packages(settings.PROJECTS_DIR):
            client_dir = os.path.join(pkg_dir, 'client')
            if not os.path.isdir(client_dir):
                break

            for fpath in _fwalk(client_dir):
                for handler in filetype_handlers:
                    dest_dir = os.path.join(ns.build_dir, pkg_dir)
                    ns.dest_dir = dest_dir
                    if handler(fpath, ns) == True:
                        break
