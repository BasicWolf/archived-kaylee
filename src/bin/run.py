import os, sys
import argparse

def setup():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, os.path.join(root_dir, 'frontends'))
    sys.path.insert(0, os.path.join(root_dir, 'projects'))
    sys.path.insert(0, root_dir)
    os.environ['KAYLEE_SETTINGS_PATH'] = os.path.join(root_dir, 'settings/settings.py')


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
