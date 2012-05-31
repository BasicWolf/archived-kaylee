# -*- coding: utf-8 -*-

PROJECTS_DIR = '/home/zaur/Documents/projects/kaylee/src/projects'
KAYLEE_JS_ROOT = '/static/js/kaylee'
LIB_JS_ROOT    = '/static/js/lib'
PROJECTS_STATIC_ROOT = '/static/js/projects'

NODES_STORAGE = {
    'name' : 'MemoryNodesStorage',
    'config' : {},
}

APPLICATIONS = [
    { 'name' : 'mc_pi.1',
      'description' : 'Find value of Pi via the Monte-Carlo method.',
      'project' : {
            'name' : 'MonteCarloPiProject',
            'config' : {
                'script' : 'monte_carlo_pi/monte_carlo_pi.js',
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
