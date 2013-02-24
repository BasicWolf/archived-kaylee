import os
import argparse
import shutil
from jinja2 import Template
from kaylee.manager import AdminCommand
from kaylee.util import random_string

ENV_TEMPLATE_DIR = 'templates/env_template'
ENV_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__),
                                     ENV_TEMPLATE_DIR)

TEMPLATE_FILES = [
    'klmanage.py',
    'settings.py',
]


class StartEnvCommand(AdminCommand):
    name = 'startenv'
    help = 'Creates Kaylee environment.'

    args = {
        'name' : {},
    }

    @staticmethod
    def execute(ns):
        secret_key = random_string(32)

        dest_path = os.path.join(os.getcwd(), ns.name)
        shutil.copytree(ENV_TEMPLATE_PATH, dest_path)

        render_args = {
            'SECRET_KEY' : secret_key,
            'PROJECTS_DIR' : dest_path,
        }

        for fname in TEMPLATE_FILES:
            template_path = os.path.join(dest_path, fname)
            with open(template_path) as f:
                template_data = f.read()
            document_data = Template(template_data).render(**render_args)
            doc_path = os.path.join(dest_path, fname)
            with open(doc_path, 'w') as f:
                f.write(document_data)

        print('Kaylee environment "{}" has been successfully created.'.format(
                ns.name))
