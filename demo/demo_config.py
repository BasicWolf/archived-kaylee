# -*- coding: utf-8 -*-
import os


REGISTRY = {
    'name' : 'MemoryNodesRegistry',
    'config' : {
        'timeout' : '30m'
    },
}

PROJECTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            'projects'))
WORKER_SCRIPT = '/static/js/kaylee/klworker.js'

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
            'name' : 'MemoryPermanentStorage',
            },
        },
    'controller' : {
        'name' : 'SimpleController',
        'filters' : {
            'accept_result' : ['kaylee.controller.failed_result_filter', ] ,
            }
        }
    }

APPLICATIONS = [app_hash_cracker_1]
