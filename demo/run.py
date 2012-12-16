#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import logging

log = logging.getLogger(__name__)

_pjoin = os.path.join
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    parser = argparse.ArgumentParser(description='Kaylee demo launcher')
    parser.add_argument('-f', '--frontend', default = 'flask',
                        choices = ['flask', 'django'])
    args = parser.parse_args()

    check_env()
    setup()

    if args.frontend == 'flask':
        from flask_launcher import run
    elif args.frontend == 'django':
        from django_launcher import run
    run()


def check_env():
    if not os.path.exists(_pjoin(CURRENT_DIR, 'build')):
        log.warn('The "build" directory was not found. '
                 'Has the demo been built?')

    try:
        import Image
    except ImportError:
        log.warn('Python Imaging Library is not installed. It is required '
                 'by the HumanOCR demo application in order to run properly.'
                 '\nRun "pip install pil" to install PIL.')

def setup():
    logging.basicConfig(level = logging.DEBUG)

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, _pjoin(CURRENT_DIR, 'launchers'))
    sys.path.insert(0, _pjoin(CURRENT_DIR, 'launchers/django_launcher'))
    sys.path.insert(0, _pjoin(CURRENT_DIR, 'projects'))
    sys.path.insert(0, _pjoin(CURRENT_DIR, '../'))

    import kaylee
    kaylee.setup(_pjoin(CURRENT_DIR, 'demo_config.py'))

    # module mock
    class KayleeDemo(object):
        FRONTEND_TEMPLATES_DIR = _pjoin(CURRENT_DIR, 'build/templates')
        FRONTEND_STATIC_DIR = _pjoin(CURRENT_DIR, 'build/static')
    sys.modules['kaylee_demo'] = KayleeDemo

if __name__ == '__main__':
    main()
