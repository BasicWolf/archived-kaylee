# -*- coding: utf-8 -*-

DEBUG = True

REGISTRY = {
    'name' : 'MemoryNodesRegistry',
    'config' : {
        # timeout format: 1d 12h 10m 5s, e.g. "12h"; "1d 10m" etc.
        'timeout' : '12h'
        },
}

PROJECTS_DIR = '/home/zaur/Documents/projects/kaylee/src/projects'
KAYLEE_WORKER_SCRIPT = '/static/js/kaylee/klworker.js'

# Settings used for Kaylee front-end demonstration
FRONTEND_TEMPLATES_DIR = '/home/zaur/Documents/projects/kaylee/src/demo_build' \
                         '/templates'
FRONTEND_STATIC_DIR = '/home/zaur/Documents/projects/kaylee/src/demo_build' \
                      '/static'


## User applications ##
#######################

app_hash_cracker_1 = {
    'name' : 'hash_cracker.1',
    'description' : 'Crack a salted hash',
    'project' : {
        'name' : 'HashCrackerProject',
        'config' : {
            'script'        : '/static/js/projects/hash_cracker/hash_cracker.js',
            'md5_script'    : '/static/js/projects/hash_cracker/md5.js',
            'hash_to_crack' : '71eebe6997feec5cd4d570c1b15ae786', # md5('klsalt')
            'salt'          : 'salt',
            'alphabet'      : 'abcdefghijklmopqrstuvwxyz',
            # although knowing the length of the key is a cheat,
            # but it's fine enough for demo purposes
            'key_length'    : 2,
            'hashes_per_task' : 100,
            },
        'storage' : {
            'name' : 'MemoryProjectResultsStorage',
            },
        },
    'controller' : {
        'name' : 'SimpleController',
        'filters' : {
            'accept_result' : 'kaylee.controller.failed_result_filter',
            }
        }
    }

app_mc_pi_1 = {
    'name' : 'mc_pi.1',
    'description' : 'Find value of Pi via the Monte-Carlo method.',
    'project' : {
        'name' : 'MonteCarloPiProject',
        'config' : {
            'script' : '/static/js/projects/monte_carlo_pi/monte_carlo_pi.js',
            'alea_script' : '/static/js/projects/monte_carlo_pi/alea.js',
            'random_points' : 1000000,
            'tasks_count' : 4
            },
        'storage' : {
            'name' : 'MemoryProjectResultsStorage',
            'config' : {},
            }
        },
    'controller' : {
        'name' : 'ResultsComparatorController',
        'config' : {
            'comparison_nodes': 2
            },
        'storage' : {
            'name' : 'MemoryControllerResultsStorage',
            'config' : {},
            },
        },
    }

APPLICATIONS = [app_hash_cracker_1]
#APPLICATIONS = [app_mc_pi_1, ]
#APPLICATIONS = [app_mc_pi_1, app_hash_cracker_1]
