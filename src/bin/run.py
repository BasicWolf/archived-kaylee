# -*- coding: utf-8 -*-
import os, sys
import argparse

def setup():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(cur_dir, '..')
    sys.path.insert(0, os.path.join(root_dir, 'frontends'))
    sys.path.insert(0, os.path.join(root_dir, 'projects'))
    sys.path.insert(0, os.path.join(root_dir, 'kaylee/testsuite'))
    sys.path.insert(0, root_dir)
    os.environ['KAYLEE_SETTINGS_PATH'] = os.path.join(cur_dir, 'settings.py')

def main():
    parser = argparse.ArgumentParser(description='Kaylee launcher')
    parser.add_argument('-f', '--frontend', default='flask', choices = ['flask'])
    args = parser.parse_args()

    setup()

    if args.frontend == 'flask':
        from flask_frontend import run
        run()
    elif args.frontend == 'django':
        pass

if __name__ == '__main__':
    main()
