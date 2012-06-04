# -*- coding: utf-8 -*-
import os, sys
import argparse

def setup():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(cur_dir, '..')

    sys.path.insert(0, os.path.join(cur_dir, 'django_launcher'))
    sys.path.insert(0, os.path.join(root_dir, 'projects'))
    sys.path.insert(0, os.path.join(root_dir, 'kaylee/testsuite'))
    sys.path.insert(0, root_dir)

    os.environ['KAYLEE_SETTINGS_MODULE'] = \
        os.path.join(cur_dir, 'kl_settings.py')

    from kaylee import settings
    settings._setup()

def main():
    parser = argparse.ArgumentParser(description='Kaylee launcher')
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
