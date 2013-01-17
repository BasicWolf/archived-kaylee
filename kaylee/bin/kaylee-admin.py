#!/usr/bin/env python
import os
import sys
#import kaylee
import shutil
import argparse
from jinja2 import Template


class KayleeCommand(object):
    pass

class KayleeStartProjectCommand(KayleeCommand):
    KL_PROJECT_TEMPLATE_DIR = 'project_template'
    command_text = 'startproject'

    def __init__(self, name, *args):
        if name.strip() == '':
            error_and_exit('project name is empty.')

        self.name = name
        self.template_dir_path = os.path.join(cwd, KL_PROJECT_TEMPLATE_DIR)

    def copy_project_template(self):
        cwd = self.cwd
        kl_template_dir_path = os.path.join(
            os.path(dirname(kaylee.conf.__file__)),
            KL_PROJECT_TEMPLATE_DIR)
        shutil.copytree(kl_template_dir_path, self.template_dir_path)

    def render_templates(self):
        _j = os.path.join
        tdp = self.template_dir_path

        with open(_j(tdp, 'server/project.py.template'), 'rw') as f:
#            Template.render()content = f.read()
            pass

    def rename_template_files(self):
        _j = os.path.join
        tdp = self.template_dir_path
        shutil.move(_j(tdp, 'server/project.py'),
                    _j(tdp, 'server/{}.py'.format(self.name)))
        shutil.move(_j(tdp, 'client/project.coffee'),
                    _j(tdp, 'client/{}.coffee'.format(self.name)))


COMMANDS_LIST = [KayleeStartProjectCommand, ]


def main():
    if len(sys.argv) == 1:
        show_help()
        sys.exit(0)
    else:
        command = get_command()


def get_command():
    command_arg = sys.argv[1]

    for cmd_cls in COMMANDS_LIST:
        if cmd_cls.command_text == command_arg:
            return cmd_cls(*sys.argv[2:])

    error_and_exit('Invalid command: {}'.format(command_arg))

def show_help():
    pass


def error_and_exit(message):
    print(message)
    sys.exit(1)

if __name__ == '__main__':
    main()
