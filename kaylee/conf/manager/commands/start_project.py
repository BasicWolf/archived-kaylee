import argparse
from kaylee.conf.manager import BaseCommand


class StartProjectCommand(BaseCommand):

    name = 'startproject'
    help = 'Starts new Kaylee project'

    args = {
        'name' : {}
    }

    def execute(cls, ns):
        # import pdb; pdb.set_trace();
        print ns.name
