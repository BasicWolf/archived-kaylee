# -*- coding: utf-8 -*-
from kaylee.project import Project

ALIAS = 'monte_carlo_pi'

class MonteCarloPiProject(Project):
    def __init__(self, *args, **kwargs):
        super(MonteCarloPiProject, self).__init__(*args, **kwargs)
        self.tasks_count = kwargs['tasks_count']
        self.random_points = kwargs['random_points']
        self.nodes_config = {
            'alias' : kwargs.get('alias', ALIAS),
            'random_points' : self.random_points,
            }
        self._tasks_counter = -1

    def __iter__(self):
        self._tasks_counter = -1
        return self

    def __next__(self):
        if self._tasks_counter < self.tasks_count:
            self._tasks_counter += 1
            return self[self._tasks_counter]
        else:
            raise StopIteration()

    def __getitem__(self, task_id):
        return { 'task' : { 'id' : str(task_id) } }

