# -*- coding: utf-8 -*-
import os
import argparse


class BaseCommand(object):
    #: Command help text
    name = ''
    help = ''
    args = {}

    @classmethod
    def add_sub_parser(cls, sub_parsers_object):
        if cls.name.strip() == '':
            raise ValueError('{}.name is empty.'.format(cls.__name__))

        parser = sub_parsers_object.add_parser(cls.name, description=cls.help)
        for arg, arg_opts in cls.args.items():
            if isinstance(arg, str):
                arg = [arg, ]
            parser.add_argument(*arg, **arg_opts)
        parser.set_defaults(handler=cls.execute)

    @staticmethod
    def execute(ns):
        raise NotImplementedError('The command has no execute() static method.')


class AdminCommand(BaseCommand):
    pass


class LocalCommand(BaseCommand):
    pass


class CommandsManager(object):
    help = ''
    command_class = BaseCommand

    def __init__(self):
        self.parser = argparse.ArgumentParser(description=self.help)
        self.sub_parsers = self.parser.add_subparsers(help='sub-commands help')
        # add sub-commands
        from .commands import commands_classes
        for cmd_cls in commands_classes:
            if issubclass(cmd_cls, self.command_class):
                self.add_command(cmd_cls)

    def add_command(self, cmd_cls):
        cmd_cls.add_sub_parser(self.sub_parsers)

    def parse(self, argv=None):
        ns = self.parser.parse_args(argv)
        if 'handler' in ns:
            ns.handler(ns)

    @classmethod
    def execute_from_command_line(cls):
        cls().parse()


class AdminCommandsManager(CommandsManager):
    help = 'Kaylee admin'
    command_class = AdminCommand


class LocalCommandsManager(CommandsManager):
    help = 'Kaylee local environment manager'
    command_class = LocalCommand


if __name__ == '__main__':
    main()
