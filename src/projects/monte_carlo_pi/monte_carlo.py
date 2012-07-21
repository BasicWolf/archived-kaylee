# -*- coding: utf-8 -*-
from kaylee import Project, Task
from kaylee.project import COMPLETED
from kaylee.errors import InvalidResultError


class MonteCarloPiProject(Project):
    auto_filter = True

    def __init__(self, *args, **kwargs):
        super(MonteCarloPiProject, self).__init__(*args, **kwargs)
        self.random_points = kwargs['random_points']
        self.nodes_config.update({
            'alea_script' : kwargs['alea_script'],
            'random_points' : self.random_points,
        })
        self.tasks_count = kwargs['tasks_count']
        self._tasks_counter = -1

    def __next__(self):
        if self._tasks_counter < self.tasks_count:
            self._tasks_counter += 1
            return self[self._tasks_counter]
        else:
            raise StopIteration()

    def __getitem__(self, task_id):
        return Task(task_id)

    def normalize(self, data):
        try:
            return data['pi']
        except KeyError:
            raise InvalidResultError(data, '"pi" key was not found')

    def store_result(self, task_id, data):
        super(MonteCarloPiProject, self).store_result(task_id, data)
        if len(self.storage) == self.tasks_count:
            self.completed = True
            self._announce_results()

    def _announce_results(self):
        mid_pi = sum(res for res in self.storage.values()[0]) / len(self.storage)
        print('The  value of PI computed by the Monte-Carlo method is: {}'
              .format(mid_pi))
