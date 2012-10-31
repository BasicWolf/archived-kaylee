# -*- coding: utf-8 -*-
import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
BUILD_DIR = os.path.join(CURRENT_DIR, 'build/')
STATIC_DIR = os.path.join(BUILD_DIR, 'static/')

PROJECTS_DIR = os.path.join(CURRENT_DIR, 'projects/')

WORKER_SCRIPT_URL = '/static/js/kaylee/klworker.js'

SECRET_KEY = '1234ABCabc!@{}xyz&%*'


REGISTRY = {
    'name' : 'MemoryNodesRegistry',
    'config' : {
        'timeout' : '30m'
    },
}


## User applications ##
#######################

app_hash_cracker_1 = {
    'name' : 'hash_cracker.1',
    'description' : 'Crack a salted hash',
    'project' : {
        'name' : 'HashCrackerProject',
        'config' : {
            'script'        : '/static/projects/hash_cracker/js/hash_cracker.js',
            'md5_script'    : '/static/projects/hash_cracker/js/md5.js',
            'hash_to_crack' : '71eebe6997feec5cd4d570c1b15ae786', # md5('klsalt')
            'salt'          : 'salt',
            'alphabet'      : 'abcdefghijklmnopqrstuvwxyz',
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
        # 'name' : 'SimpleController',
        'name' : 'ResultsComparatorController',
        'config' : {
            'results_count_threshold' : 2
            },
        'storage' : {
            'name' : 'MemoryTemporalStorage',
            },
        'filters' : {
            'accept_result' : ['kaylee.controller.kl_result_filter', ],
            }
        }
    }

app_hash_cracker_2 = {
    'name' : 'hash_cracker.1',
    'description' : 'Crack a salted hash',
    'project' : {
        'name' : 'HashCrackerProject',
        'config' : {
            'script'        : '/static/projects/hash_cracker/js/hash_cracker.js',
            'md5_script'    : '/static/projects/hash_cracker/js/md5.js',
            'hash_to_crack' : '71eebe6997feec5cd4d570c1b15ae786', # md5('klsalt')
            'salt'          : 'salt',
            'alphabet'      : 'abcdefghijklmnopqrstuvwxyz',
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
            'accept_result' : ['kaylee.controller.kl_result_filter', ] ,
            }
        }
    }


app_human_ocr_1 = {
    'name' : 'human_ocr.1',
    'description' : 'Involves a human in image recognition',
    'project' : {
        'name' : 'HumanOCRProject',
        'config' : {
            'script'      : '/static/projects/human_ocr/js/human_ocr.js',
            'styles'      : '/static/projects/human_ocr/css/human_ocr.css',
            'img_dir_url' : '/static/tmp/human_ocr/',
            'img_dir'     : os.path.join(STATIC_DIR, 'tmp/human_ocr/'),
            'font_path'   : ('/usr/share/fonts/truetype/ttf-dejavu/'
                             'DejaVuSans.ttf'),
        },
        'storage' : {
            'name' : 'MemoryPermanentStorage',
        },
    },
    'controller' : {
        'name' : 'SimpleController',
        'filters' : {
            'accept_result' : ['kaylee.controller.kl_result_filter', ] ,
        }
    }
}


APPLICATIONS = [app_human_ocr_1]
# APPLICATIONS = [app_hash_cracker_1]
APPLICATIONS = [app_hash_cracker_2]
