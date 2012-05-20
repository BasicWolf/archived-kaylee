# -*- coding: utf-8 -*-
from kaylee.project import Project

ALIAS = 'monte_carlo_pi'

class MonteCarloPiProject(Project):
    def __init__(self, *args, **kwargs):
        super(MonteCarloPiProject, self).__init__(*args, **kwargs)
        self.random_points = kwargs['random_points']
        self.nodes_config = {
            'alias' : kwargs.get('alias', ALIAS),
            }
        self._tid_inc = 0

    def __iter__(self):
        self._tid_inc = 0
        return self

    def __next__(self):
        pass

    def __getitem__(self, task_id):
        pass
