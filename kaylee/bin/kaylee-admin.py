#!/usr/bin/env python

import os
import sys


class KayleeCommand(object):
    pass

class KayleeStartProjectCommand(KayleeCommand):
    command_text = 'startproject'

    def __init__(self, *args):
        cwd = os.getcwd()
        


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
