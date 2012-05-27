# -*- coding: utf-8 -*-
PROJECTS_DIR = '/home/zaur/Documents/projects/kaylee/src/projects'

DISPATCHER = {
    'nodes_storage' : {
        'name' : 'MemoryNodesStorage',
        'config' : {},
        },
}

APPLICATIONS = [
    { 'name' : 'mc_pi.1',
      'description' : 'Find value of Pi via the Monte-Carlo method.',
      'project' : {
            'name' : 'MonteCarloPiProject',
            'config' : {
                'alias' : 'monte_carlo_pi',
                'random_points' : 1000000,
                'tasks_count' : 20
                },
            },
      'controller' : {
            'name' : 'ResultsComparatorController',
            'config' : {
                'comparison_nodes': 2
                },
            'results_storage' : {
                'name' : 'MemoryControllerResultsStorage',
                'config' : {},
                },
            'app_results_storage' : {
                'name' : 'MemoryAppResultsStorage',
                'config' : {},
                }
            },
      },
]

# Common front-end settings
FRONTEND_STATIC_DIR = '/home/zaur/Documents/projects/kaylee/src/kayleejs/static'
FRONTEND_TEMPLATE_DIR = '/home/zaur/Documents/projects/kaylee/src/kayleejs/templates'
