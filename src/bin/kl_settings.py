# -*- coding: utf-8 -*-

PROJECTS_DIR = '/home/zaur/Documents/projects/kaylee/src/projects'
KAYLEE_JS_ROOT = '/static/js/kaylee'
LIB_JS_ROOT    = '/static/js/lib'
PROJECTS_STATIC_ROOT = '/static/js/projects'

NODES_STORAGE = {
    'name' : 'MemoryNodesStorage',
    'config' : {
        # timeout format: 1d 12h 10m 5s, e.g. "12h"; "1d 10m" etc.
        'timeout' : '12h'
        },
}

APPLICATIONS = [
    { 'name' : 'mc_pi.1',
      'description' : 'Find value of Pi via the Monte-Carlo method.',
      'project' : {
            'name' : 'MonteCarloPiProject',
            'config' : {
                'script' : 'monte_carlo_pi/monte_carlo_pi.js',
                'random_points' : 1000000,
                'tasks_count' : 4
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

    { 'name' : 'hash_cracker.1',
      'description' : 'Crack a salted hash',
      'project' : {
            'name' : 'HashCrackerProject',
            'config' : {
                'script' : 'hash_cracker/hash_cracker.js',
                'alphabet' : 'abcdefghijklmopqrstuvwxyz',
                'key_length' : (4, 5),
                'hash_func' : 'md5(md5(k) + s)',
                'hashes_per_task' : 100,
                }
            },
      'controller' : {
            'name' :'SimpleController',
            'app_results_storage' : {
                'name' : 'MemoryAppResultsStorage',
                }
            }
      },
]


# Settings used for Kaylee front-end demonstration
FRONTEND_TEMPLATES_DIR = '/home/zaur/Documents/projects/kaylee/src/kayleejs/templates'
FRONTEND_STATIC_DIR = '/home/zaur/Documents/projects/kaylee/src/kayleejs/static'
