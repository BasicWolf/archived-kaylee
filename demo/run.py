#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import logging

def setup():
    logging.basicConfig(level = logging.DEBUG)

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(cur_dir, 'launchers'))
    sys.path.insert(0, os.path.join(cur_dir, 'launchers/django_launcher'))
    sys.path.insert(0, os.path.join(cur_dir, 'projects'))
    sys.path.insert(0, os.path.join(cur_dir, '../'))

    import kaylee
    kaylee.setup(os.path.join(cur_dir, 'demo_config.py'))

    # module mock
    class KayleeDemo(object):
        FRONTEND_TEMPLATES_DIR = os.path.join(cur_dir, 'build/templates')
        FRONTEND_STATIC_DIR = os.path.join(cur_dir, 'build/static')
    sys.modules['kaylee_demo'] = KayleeDemo

def main():
    parser = argparse.ArgumentParser(description='Kaylee demo launcher')
    parser.add_argument('-f', '--frontend', default = 'flask',
                        choices = ['flask', 'django'])
    args = parser.parse_args()

    setup()

    if args.frontend == 'flask':
        from flask_launcher import run
    elif args.frontend == 'django':
        from django_launcher import run
    run()




if __name__ == '__main__':
    main()
