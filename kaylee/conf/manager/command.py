# -*- coding: utf-8 -*-
import os
import argparse
from abc import ABCMeta, abstractmethod


class BaseCommand(object):
    __metaclass__ = ABCMeta

    #: Command help text
    help = ''
    name = ''
    args = {}

    def __init__(self, parser):
        for arg, arg_opts in self.args.items():
            if isinstance(arg, str):
                arg = [arg, ]
            parser.add_argument(*arg, **arg_opts)

    @abstractmethod
    def execute(self, ns):
        pass

class CommandsManager(object):
    help = 'Kaylee manager'

    def __init__(self):
        self.parser = argparse.ArgumentParser(description=self.help)
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
        if cmd_cls.name.strip() == '':
            raise ValueError('{}.name is empty.'.format(cmd_cls.__name__))
        cmd_parser = self.sub_parsers.add_parser(cmd_cls.name)
        cmd = cmd_cls(cmd_parser)

    def parse(self, argv):
        self.parser.parse_args(argv)
