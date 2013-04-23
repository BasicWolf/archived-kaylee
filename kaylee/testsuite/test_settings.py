# -*- coding: utf-8 -*-

from kaylee.testsuite import  PROJECTS_DIR

AUTO_GET_ACTION = True

PROJECTS_DIR = PROJECTS_DIR

SECRET_KEY = 'aJD2fn;1340913)*(!!&$)(#&<AHFB12b'

REGISTRY = {
    'name' : 'MemoryNodesRegistry',
    'config' : {
        'timeout' : '2s',
        },
}

APPLICATIONS = [
    { 'name' : 'test.1',
      'description' : 'Test application',
      'project' : {
            'name' : 'AutoTestProject',
            },
      'controller' : {
            'name' :'TestController1',
            'config' : {},
            'temporal_storage' : {
                'name' : 'MemoryTemporalStorage',
                },
            'permanent_storage' : {
                'name' : 'MemoryPermanentStorage',
                },
            },
      }
    ]
