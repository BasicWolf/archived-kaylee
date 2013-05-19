from __future__ import print_function
import os
import sys
import imp
import importlib
import subprocess
import shutil
import kaylee
from kaylee.manager import LocalCommand
from kaylee.loader import find_packages, get_classes_from_module
from kaylee.util import ensure_dir


class BuildCommand(LocalCommand):
    name = 'build'
    help = 'Builds Kaylee environment'

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
        build_kaylee(opts)
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


def build_kaylee(opts):
    print('* Copying Kaylee test server files...')
    KLCL_TEMPLATE_DIR = 'templates/build_template'
    KLCL_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__),
                                      KLCL_TEMPLATE_DIR)

    KLCL_CLIENT_PATH = os.path.join(os.path.dirname(kaylee.__file__),
                                    'client')
    CLIENT_FILES = [
        ('kaylee.js', 'kaylee/js/kaylee.js'),
        ('klworker.js', 'kaylee/js/klworker.js'),
    ]

    TEMPLATE_FILES = [
        ('css/klconsole.css', 'kaylee/css/klconsole.css'),
        ('js/kldebug.js', 'kaylee/js/kldebug.js'),
        ('js/jquery.min.js', 'kaylee/js/jquery.min.js'),
        ('index.html', 'index.html'),
    ]

    dest_path = os.path.join(os.getcwd(), opts.build_dir)
    ensure_dir(os.path.join(dest_path, 'kaylee/js'))
    ensure_dir(os.path.join(dest_path, 'kaylee/css'))

    for fname, out_fname in CLIENT_FILES:
        fpath = os.path.join(KLCL_CLIENT_PATH, fname)
        dest_fpath = os.path.join(dest_path, out_fname)
        shutil.copy(fpath, dest_fpath)

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

    # Make sure that the command is able to import the projects'
    # Python packages.
    sys.path.insert(0, settings.PROJECTS_DIR)

    for pkg_dir in find_packages(settings.PROJECTS_DIR):
        if not is_kaylee_project_directory(pkg_dir):
            continue
        print('* Building {}...'.format(pkg_dir))
        dest_dir = os.path.join(opts.build_dir, pkg_dir)
        opts.dest_dir = dest_dir
        # clear destination directory before building
        if os.path.isdir(dest_dir):
            shutil.rmtree(dest_dir)
        # build project client by applying appropriate
        # file handlers
        client_dir = os.path.join(pkg_dir, 'client')
        for fname in os.listdir(client_dir):
            fpath = os.path.join(client_dir, fname)
            if not os.path.isfile(fpath):
                continue
            for handler in filetype_handlers:
                if handler(fpath, opts) == True:
                    break

def is_kaylee_project_directory(path):
    # check if 'client' directory exists
    client_dir = os.path.join(path, 'client')
    if not os.path.isdir(client_dir):
        return False
    # check for kaylee.Project subclass
    package_name = path.rsplit('/')[-1]
    pymod = importlib.import_module(package_name)
    for cls in get_classes_from_module(pymod):
        if issubclass(cls, kaylee.project.Project):
            return True
    return False

def coffee_handler(fpath, opts):
    if not fpath.endswith('.coffee'):
        return False

    args = ['coffee', '--bare', '-c', fpath]
    proc = subprocess.Popen(args,
                            close_fds=True,
                            stdin=subprocess.PIPE,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE)
    #pylint: disable-msg=W0612
    #W0612: Unused variable 'stdoutdata'
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
