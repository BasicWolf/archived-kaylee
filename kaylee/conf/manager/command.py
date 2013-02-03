# -*- coding: utf-8 -*-
import os
import argparse
from abc import ABCMeta, abstractmethod


class BaseCommand(object):
    __metaclass__ = ABCMeta

    #: Command help text
    help = ''
    args = {}

    @abstractmethod
    def __init__(self, parser):
        pass


class CommandsManager(object):
    help = 'Kaylee manager'

    def __init__(self):
        self.parser = argparse.ArgumentParser(description=self.help)



    def parse(self, argv):
        self.parser.parse_args(argv)

