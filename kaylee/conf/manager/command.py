# -*- coding: utf-8 -*-
import os
import sys
import argparse


class BaseCommand(object):
    #: Command help text
    help = ''
    name = ''
    args = {}

    @classmethod
    def add_sub_parser(cls, sub_parsers):
        if cls.name.strip() == '':
            raise ValueError('{}.name is empty.'.format(cls.__name__))

        parser = sub_parsers.add_parser(cls.name)
        for arg, arg_opts in cls.args.items():
            if isinstance(arg, str):
                arg = [arg, ]
            parser.add_argument(*arg, **arg_opts)
        parser.set_defaults(func=cls.execute)

    @classmethod
    def execute(cls, ns):
        pass


class CommandsManager(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Kaylee manager')
        self.sub_parsers = self.parser.add_subparsers(help='sub-commands help')
        # add sub-commands
        from .commands import commands_classes
        for cmd_cls in commands_classes:
            self.add_command(cmd_cls)

    def add_command(self, cmd_cls):
        if not issubclass(cmd_cls, BaseCommand):
            raise TypeError('cmd_cls must be a subclass of {}, not {}'
                            .format(BaseCommand.__name__,
                                    type(cmd_cls).__name__))
        cmd_cls.add_sub_parser(self.sub_parsers)

    def parse(self, argv):
        self.parser.parse_args(argv)



def execute_from_command_line():
    manager = CommandsManager()
    manager.parse(sys.argv)

if __name__ == '__main__':
    main()
