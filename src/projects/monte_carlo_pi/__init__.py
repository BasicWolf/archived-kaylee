from kaylee.project import Project

class MonteCarloPiProject(Project):
    def __init__(self, *args, **kwargs):
        super(MonteCarloPiProject, self).__init__(*args, **kwargs)
        self.random_points = kwargs['random_points']
        self.node_config = {
            'alias' : kwargs.get('alias', 'monte_carlo_pi'),
            'random_points' : self.random_points,
            }

