import os
import re
import argparse
import shutil
from jinja2 import Template
from kaylee.server import run
from kaylee.manager import LocalCommand


class RunCommand(LocalCommand):
    name = 'run'
    help = 'Runs Kaylee development/testing server'

    args = {

    }

    @staticmethod
    def execute(ns):
        print('Launching Kaylee development/testing server...')
        run(os.environ.get('KAYLEE_SETTINGS_PATH'))
