# -*- coding: utf-8 -*-

app_hash_cracker_1 = {
    'name' : 'hash_cracker.1',
    'description' : 'Crack a salted hash',
    'project' : {
        'name' : 'HashCrackerProject',
        'config' : {
            'script' : 'hash_cracker/hash_cracker.js',
            'hash_to_crack' : '9b630e300e46c67c8f4ab07522b469c7',
            'salt'          : 'klsalt',
            'alphabet'      : 'abcdefghijklmopqrstuvwxyz',
            'hash_func'     : 'md5(md5(k) + s)',
            # although knowing the length of the key is a cheat,
            # but it's fine enough for demo purposes
            'key_length'    : 4,
            'hashes_per_task' : 100,
            }
        },
    'controller' : {
        'name' : 'SimpleController',
        'app_storage' : {
            'name' : 'MemoryAppResultsStorage',
            }
        }
    }

app_mc_pi_1 = {
    'name' : 'mc_pi.1',
    'description' : 'Find value of Pi via the Monte-Carlo method.',
    'project' : {
        'name' : 'MonteCarloPiProject',
        'config' : {
            'script' : 'monte_carlo_pi/monte_carlo_pi.js',
            'random_points' : 1000000,
            'tasks_count' : 3
            },
        },
    'controller' : {
        'name' : 'ResultsComparatorController',
        'config' : {
            'comparison_nodes': 3
            },
        'tmp_storage' : {
            'name' : 'MemoryControllerResultsStorage',
            'config' : {},
            },
        'app_storage' : {
            'name' : 'MemoryAppResultsStorage',
            'config' : {},
            }
        },
    }

APPLICATIONS = [app_mc_pi_1, app_hash_cracker_1]

NODES_STORAGE = {
    'name' : 'MemoryNodesStorage',
    'config' : {
        # timeout format: 1d 12h 10m 5s, e.g. "12h"; "1d 10m" etc.
        'timeout' : '12h'
        },
}

PROJECTS_DIR = '/home/zaur/Documents/projects/kaylee/src/projects'
KAYLEE_JS_ROOT = '/static/js/kaylee'
LIB_JS_ROOT    = '/static/js/lib'
PROJECTS_STATIC_ROOT = '/static/js/projects'


# Settings used for Kaylee front-end demonstration
FRONTEND_TEMPLATES_DIR = '/home/zaur/Documents/projects/kaylee/src/kayleejs/templates'
FRONTEND_STATIC_DIR = '/home/zaur/Documents/projects/kaylee/src/kayleejs/static'
