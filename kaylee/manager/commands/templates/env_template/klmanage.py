#!/usr/bin/env python
import os

def main():
    from kaylee.manager import LocalCommandsManager

    CURRENT_DIR = os.path.dirname(__file__)
    settings_path = os.path.join(CURRENT_DIR, 'settings.py')
    os.environ.setdefault('KAYLEE_SETTINGS_PATH', settings_path)

    LocalCommandsManager.execute_from_command_line()

if __name__ == '__main__':
    main()
