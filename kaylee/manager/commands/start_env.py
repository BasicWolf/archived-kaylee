import os
import stat
from jinja2 import Template
from kaylee.manager import AdminCommand
from kaylee.util import random_string


class StartEnvCommand(AdminCommand):
    name = 'startenv'
    help = 'Creates Kaylee environment.'

    args = {
        'name' : {},
    }

    @staticmethod
    def execute(opts):
        start_env(opts)

#pylint: disable-msg=R0914
#R0914: 21,0:start_env: Too many local variables (16/15)
def start_env(opts):
    ENV_TEMPLATE_DIR = 'templates/env_template'
    ENV_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__),
                                     ENV_TEMPLATE_DIR)
    TEMPLATE_FILES = [
        # see notes about klmanage.py below
        ('klmanage.py', 'klmanage.py'),
        ('settings.py', 'settings.py'),
    ]

    if opts.name == '.':
        dest_path = os.getcwd()
    else:
        dest_path = os.path.join(os.getcwd(), opts.name)
        os.mkdir(dest_path)

    render_args = {
        'SECRET_KEY' : random_string(32),
        'PROJECTS_DIR' : dest_path,
    }

    for fname, out_fname in TEMPLATE_FILES:
        template_path = os.path.join(ENV_TEMPLATE_PATH, fname)
        with open(template_path) as f:
            template_data = f.read()
        document_data = Template(template_data).render(**render_args)
        out_path = os.path.join(dest_path, out_fname)
        with open(out_path, 'w') as f:
            f.write(document_data)

    # explicitly chmod +x klmanage.py
    klmanage_path = os.path.join(dest_path, 'klmanage.py')
    st = os.stat(klmanage_path)
    os.chmod(klmanage_path, st.st_mode | stat.S_IEXEC)

    _dirname = 'current directory' if opts.name == '.' else opts.name
    print('Kaylee environment has been successfully created in {}'
          .format(_dirname))
