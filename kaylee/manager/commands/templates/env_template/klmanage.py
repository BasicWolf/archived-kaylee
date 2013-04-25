#!/usr/bin/env python

def main():
    from kaylee.manager import LocalCommandsManager
    LocalCommandsManager.execute_from_command_line()

if __name__ == '__main__':
    main()
