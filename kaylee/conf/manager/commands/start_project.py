import argparse
from kaylee.conf.manager import BaseCommand


class StartProjectCommand(BaseCommand):

    help = 'Starts new Kaylee project'
    args = {}

    def __init__(self, parser):
        pass
