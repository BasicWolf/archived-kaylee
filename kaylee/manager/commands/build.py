from __future__ import print_function
import os
import sys
import re
import argparse
import shutil
from kaylee.manager import LocalCommand

import logging
log = logging.getLogger(__name__)


class BuildCommand(LocalCommand):
    name = 'build'
    help = 'Build Kaylee environment'

    args = {
        ('-p', '--projects-dir') : dict(default='.'),
        ('-b', '--build-dir') : dict(default='_build')
    }

    @staticmethod
    def execute(ns):
        print('Building Kaylee environment...')

        # 1. Scan projects-dir for sub-directories with __init__.py
        # 2. Scan found __init__.py for project classes
        # 3. Build the client as follows:
        #    os.walk() the client dir
        #    for each coffee file - compile it
        #    move every file to corresponding directory
        #    e.g. '.js' to 'js', '.css' to 'css', '.png/.jpg/etc.' to 'img'
        #       the rest - move to 'data'. Make sure that these options are
        #       configurable through command-line.
         
