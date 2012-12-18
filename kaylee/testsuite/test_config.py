#pylint: disable-all
from kaylee.testsuite import  PROJECTS_DIR


WORKER_SCRIPT_URL = '/static/js/kaylee/klworker.js'

PROJECTS_DIR = PROJECTS_DIR

SECRET_KEY = 'aJD2fn;1340913)*(!!&$)(#&<AHFB12b'

REGISTRY = {
    'name' : 'MemoryNodesRegistry',
    'config' : {
        'timeout' : '2s',
        },
}

APPLICATIONS = [
    { 'name' : 'dummy.1',
      'description' : 'Dummy application',
      'project' : {
            'name' : 'DummyProject',
            },
      'controller' : {
            'name' :'DummyController',
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
