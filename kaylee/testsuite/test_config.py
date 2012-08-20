from kaylee.testsuite import  PROJECTS_DIR


WORKER_SCRIPT = '/static/js/kaylee/klworker.js'

PROJECTS_DIR = PROJECTS_DIR


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
            'storage' : {
                'name' : 'MemoryTemporalStorage',
                },
            'app_storage' : {
                'name' : 'MemoryPermanentStorage',
                },
            },
      }
    ]
