# -*- coding: utf-8 -*-
PROJECTS_DIR = '/home/zaur/Documents/projects/kaylee/src/projects'

APPLICATIONS = [
    { 'name' : 'mc_pi.1',
      'description' : 'description here',
      'project' : {
            'name' : 'MonteCarloPiProject',
            'config' : {
                'alias' : 'monte_carlo_pi',
                'random_points' : 10000,
                }
            },
      'controller' : {
            'name' : 'ResultsComparatorController',
            'config' : {
                'comparison_nodes': 2
                },
            'nodes_storage' : {
                'name' : 'MemoryNodesStorage',
                'config' : {},
                }
            },
      },
]

# Common front-end settings
FRONTEND_STATIC_DIR = '/home/zaur/Documents/projects/kaylee/src/kayleejs/static'
FRONTEND_TEMPLATE_DIR = '/home/zaur/Documents/projects/kaylee/src/kayleejs/templates'
