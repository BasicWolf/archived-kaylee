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


class BuildCommand(LocalCommand):
    name = 'build'
    help = 'Build Kaylee environment'

    args = {
        ('-s', '--settings-file') : dict(default='settings.py'),
        ('-b', '--build-dir') : dict(default='_build')
    }

    @staticmethod
    def execute(opts):
        verify_settings(opts)
        verify_build_dir(opts)

        print('Building Kaylee environment...')
        settings = imp.load_source('settings', opts.settings_file)
        build_kaylee(settings, opts)
        build_projects(settings, opts)


def verify_settings(opts):
    if not os.path.exists(opts.settings_file):
        raise OSError('Cannot find the settings file "{}"'
                      .format(opts.settings_file))

def verify_build_dir(opts):
    try:
        if not os.path.exists(opts.build_dir):
            os.mkdir(opts.build_dir)
    except OSError as e:
        raise OSError('Failed to create build directory {}: {}'
                      .format(opts.build_dir, e))


def build_kaylee(settings, opts):
    print('Copying Kaylee test server files...')
    KLCL_TEMPLATE_DIR = 'templates/build_template'
    KLCL_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__),
                                      KLCL_TEMPLATE_DIR)
    TEMPLATE_FILES = [
        ('klconsole.js', 'kaylee/js/klconsole.js'),
        ('kldemo.js', 'kaylee/js/kldemo.js'),
        ('index.html', 'index.html'),
    ]

    dest_path = os.path.join(os.getcwd(), opts.build_dir)
    ensure_dir(os.path.join(dest_path, 'kaylee/js'))
    for fname, out_fname in TEMPLATE_FILES:
        fpath = os.path.join(KLCL_TEMPLATE_PATH, fname)
        dest_fpath = os.path.join(dest_path, out_fname)
        shutil.copy(fpath, dest_fpath)


def build_projects(settings, opts):
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

        print('Building {}...'.format(pkg_dir))
        dest_dir = os.path.join(opts.build_dir, pkg_dir)
        opts.dest_dir = dest_dir
        # clear destination directory before building
        if os.path.isdir(dest_dir):
            shutil.rmtree(dest_dir)
        # build project client by applying appropriate
        # file handlers
        for fpath in _fwalk(client_dir):
            for handler in filetype_handlers:
                if handler(fpath, opts) == True:
                    break


def coffee_handler(fpath, opts):
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

    dest_dir = os.path.join(opts.dest_dir, 'js')
    ensure_dir(dest_dir)
    outpath = fpath.rsplit('.coffee', 1)[0] + '.js'
    shutil.move(outpath, dest_dir)
    return True


def script_handler(fpath, opts):
    if not fpath.endswith('.js'):
        return False

    dest_dir = os.path.join(opts.dest_dir, 'js')
    ensure_dir(dest_dir)
    shutil.copy(fpath, dest_dir)
    return True


def stylesheet_handler(fpath, opts):
    if not fpath.endswith('.css'):
        return False

    dest_dir = os.path.join(opts.dest_dir, 'css')
    ensure_dir(dest_dir)
    shutil.copy(fpath, dest_dir)
    return True


def data_handler(fpath, opts):
    dest_dir = os.path.join(opts.dest_dir, 'data')
    ensure_dir(dest_dir)
    shutil.copy(fpath, dest_dir)
    return True

