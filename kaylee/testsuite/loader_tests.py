from kaylee.testsuite import KayleeTest, load_tests, PROJECTS_DIR

import os
from kaylee import loader, Kaylee
from kaylee.contrib import (MemoryTemporalStorage,
                            MemoryPermanentStorage,
                            MemoryNodesRegistry)

_test_REGISTRY = {
    'name' : 'MemoryNodesRegistry',
    'config' : {
        'timeout' : '2s',
        },
}


class TestConfig(object):
    REGISTRY = _test_REGISTRY
    WORKER_SCRIPT = '/static/js/kaylee/klworker.js'

class TestConfigWithApps(object):
    REGISTRY = _test_REGISTRY
    WORKER_SCRIPT = '/static/js/kaylee/klworker.js'
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

    PROJECTS_DIR = PROJECTS_DIR

class KayleeLoaderTests(KayleeTest):
    def test_load_config_class(self):
        kl = loader.load(TestConfig)
        self.assertIsInstance(kl, Kaylee)
        self.assertEqual(kl.config.WORKER_SCRIPT, TestConfig.WORKER_SCRIPT)

    def test_load_config_dict(self):
        kl = loader.load(dict(TestConfig.__dict__))
        self.assertIsInstance(kl, Kaylee)
        self.assertEqual(kl.config.WORKER_SCRIPT, TestConfig.WORKER_SCRIPT)

    def test_load_config_module(self):
        import test_config
        kl = loader.load(test_config)
        self.assertIsInstance(kl, Kaylee)
        self.assertEqual(kl.config.WORKER_SCRIPT, test_config.WORKER_SCRIPT)

    def test_load_config_path(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_config.py'))
        kl = loader.load(path)
        import test_config
        self.assertIsInstance(kl, Kaylee)
        self.assertEqual(kl.config.WORKER_SCRIPT, test_config.WORKER_SCRIPT)

    def test_load_applications(self):
        config = dict(TestConfigWithApps.__dict__)
        loader.refresh(config)
        apps = loader.load_applications(config)
        self.assertIsInstance(apps, list)
        self.assertEqual(len(apps), 1)

        app = apps[0]
        self.assertEqual(app.__class__.__name__, 'DummyController')
        self.assertEqual(app.project.__class__.__name__, 'DummyProject')
        self.assertIsInstance(app.storage, MemoryTemporalStorage)
        #self.assertIsInstance(app.project.storage, MemoryPermanentStorage)

    def test_load_registry(self):
        config = dict(TestConfig.__dict__)
        loader.refresh(config)
        reg = loader._load_registry(config)
        self.assertIsInstance(reg, MemoryNodesRegistry)

    def test_load_kaylee(self):
        kl = loader.load(TestConfigWithApps)
        self.assertIsInstance(kl.registry, MemoryNodesRegistry)

        app = kl.applications['dummy.1']
        self.assertEqual(app.__class__.__name__, 'DummyController')
        self.assertEqual(app.project.__class__.__name__, 'DummyProject')

    def test_kaylee_setup(self):
        from kaylee import setup, kl
        self.assertIsNone(kl._wrapped)
        setup(TestConfigWithApps)

        self.assertIsNotNone(kl._wrapped)
        self.assertIsInstance(kl.registry, MemoryNodesRegistry)

        app = kl.applications['dummy.1']
        self.assertEqual(app.__class__.__name__, 'DummyController')
        self.assertEqual(app.project.__class__.__name__, 'DummyProject')


kaylee_suite = load_tests([KayleeLoaderTests])
