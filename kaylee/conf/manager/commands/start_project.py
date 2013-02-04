import argparse
from kaylee.conf.manager import BaseCommand


class StartProjectCommand(BaseCommand):

    name = 'startproject'
    help = 'Starts new Kaylee project'
    args = {
        'name' : {}
    }

    def __init__(self, parser):
        pass

    def execute(self, ns):
        pass
