import os
import re
import shutil
from jinja2 import Template
from kaylee.manager import LocalCommand

# TODO: check other commands for shutil.copytree

class StartProjectCommand(LocalCommand):
    name = 'startproject'
    help = 'Starts new Kaylee project'

    args = {
        'name' : {},
        ('-m', '--mode') : dict(
            choices=['manual', 'auto'],
            default='auto',
            help="project mode",
        ),
        ('-t', '--template') : dict(
            choices=['js', 'coffee'],
            default='js',
            help="client-side programming language.",
        ),
    }

    @staticmethod
    def execute(opts):
        validate_name(opts)
        start_project(opts)


def validate_name(opts):
    if re.match(r'^\w+$', opts.name) is None:
        raise ValueError('Invalid project name: {} ([A-Za-z0-9_])'
                         .format(opts.name))


def start_project(opts):
    PROJECT_TEMPLATE_DIR = 'templates/project_template'
    PROJECT_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__),
                                         PROJECT_TEMPLATE_DIR)
    TEMPLATE_FILES = [
        #(template file in PROJECT_TEMPLATE_DIR,
        # destination file name with {project} macro replacement)
        # e.g. ('project.py', '{project_name}.py'),
        ('__init__.py.template', '__init__.py'),
        ('project.py.template', '{project_name}.py'),
        _client_template_files(opts)
    ]

    # build rendering environment constants
    project_file_name = opts.name.lower()

    # copy project template to cwd
    dest_path = os.path.join(os.getcwd(), project_file_name)

    render_args = {
        'project_file_name' : project_file_name,
        'project_class_name' : (opts.name[0].upper() + opts.name[1:]),
        'project_mode' : expand_project_mode_opt(opts.mode),
    }

    for fname, out_fname_template in TEMPLATE_FILES:
        # render template
        template_path = os.path.join(PROJECT_TEMPLATE_PATH, fname)
        with open(template_path) as f:
            template_data = f.read()
        document_data = Template(template_data).render(**render_args)

        # write to output file
        out_fname = out_fname_template.format(project_name=project_file_name)
        out_path = os.path.join(dest_path, out_fname)
        dest_dir = os.path.dirname(out_path)
        try:
            os.makedirs(dest_dir)
        except:
            pass

        with open(out_path, 'w') as f:
            f.write(document_data)
        shutil.copymode(template_path, out_path)

    print('Kaylee project "{}" was created.'.format(
            opts.name))


def _client_template_files(opts):
    template = opts.template

    if template == 'js':
        return ('client/project.js', 'client/{project_name}.js')
    elif template == 'coffee':
        return ('client/project.coffee', 'client/{project_name}.coffee')

def expand_project_mode_opt(opt):
    if opt == 'manual':
        return 'MANUAL_PROJECT_MODE'
    elif opt == 'auto':
        return 'AUTO_PROJECT_MODE'
    else:
        raise ValueError('Invalid project mode option: {}'.format(opt))
