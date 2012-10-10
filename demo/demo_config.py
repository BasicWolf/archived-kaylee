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

SECRET_KEY = '1234ABCabc!@{}xyz&%*'

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
            'accept_result' : ['kaylee.controller.failed_result_filter', ] ,
            }
        }
    }


app_human_ocr_1 = {
    'name' : 'human_ocr.1',
    'description' : 'Involves a human in image recognition',
    'project' : {
        'name' : 'HumanOCRProject',
        'config' : {
            'script'    : '/static/js/projects/hash_cracker/human_ocr.js',
            'img_dir_url' : '/static/tmp/human_ocr/',
            'img_dir'     : os.path.join(STATIC_DIR, 'tmp/human_ocr/'),
            'font_path' : ('/usr/share/fonts/truetype/ttf-dejavu/'
                           'DejaVuSans.ttf'),
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
