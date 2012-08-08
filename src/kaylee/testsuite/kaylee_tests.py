# -*- coding: utf-8 -*-
import os
import json

import dummy_settings
from projects.dummy_project.dummy import DummyProject, DummyController
from kaylee.testsuite import KayleeTest, load_tests, TestSettings
from kaylee import (NodeID, Node, Kaylee, KayleeError, Applications, )
from kaylee.loader import _load_kaylee_objects, _load, LazySettings
from kaylee.contrib.storages import (MemoryControllerResultsStorage,
                                     MemoryProjectResultsStorage)

from kaylee.contrib.registries import MemoryNodesRegistry

from datetime import datetime


class Settings1(TestSettings):
    REGISTRY = {
        'name' : 'MemoryNodesRegistry',
        'config' : {
            'timeout' : '2s',
            },
    }

    KAYLEE_WORKER_SCRIPT = '/static/js/kaylee/klworker.js'

class Settings2(Settings1):
    APPLICATIONS = [
        { 'name' : 'dummy.1',
          'description' : 'Dummy application',
          'project' : {
                'name' : 'DummyProject',
                'config' : {}
                },
          'controller' : {
                'name' :'DummyController',
                'config' : {},
                'storage' : {
                    'name' : 'MemoryControllerResultsStorage',
                    'config' : {}
                    },
                'app_storage' : {
                    'name' : 'MemoryProjectResultsStorage',
                    'config' : {}
                    },
                },
          }
        ]


class KayleeLoaderTests(KayleeTest):
    def test_load_client_config(self):
        nconf, storage, apps = _load_kaylee_objects(Settings1)
        self.assertEqual(nconf['KAYLEE_WORKER_SCRIPT'],
                         Settings1.KAYLEE_WORKER_SCRIPT)
        self.assertEqual(len(apps), 0)

    def test_load_nodes_storage(self):
        nconf, storage, apps = _load_kaylee_objects(Settings1)
        self.assertIsInstance(storage, MemoryNodesRegistry)

    def test_load_applications(self):
        nconf, storage, apps = _load_kaylee_objects(Settings2)
        self.assertEqual(len(apps), 1)
        app = apps['dummy.1']
        self.assertEqual(app.__class__.__name__, DummyController.__name__)
        self.assertEqual(app.app_name, 'dummy.1')
        self.assertIsInstance(app.storage, MemoryControllerResultsStorage)
        self.assertEqual(app.project.__class__.__name__, DummyProject.__name__)

    def test_load_kaylee(self):
        kl = _load(Settings2)
        self.assertIn('dummy.1', kl.applications)
        self.assertIsInstance(kl.registry, MemoryNodesRegistry)

    def test_init_kaylee(self):
        project = DummyProject()
        storage = MemoryControllerResultsStorage()
        app_storage = MemoryProjectResultsStorage()
        controller = DummyController('dummy_app', project, storage, app_storage)
        apps = Applications({'dummy_app' : controller})
        kl = Kaylee({}, MemoryNodesRegistry(timeout = '2h'), apps)
        self.assertIn('dummy_app', kl.applications)
        self.assertIsInstance(kl.registry, MemoryNodesRegistry)

    def test_settings_setup(self):
        from kaylee import settings as kl_settings
        kl_settings._setup(Settings1)
        self.assertEqual(Settings1.KAYLEE_WORKER_SCRIPT,
                         kl_settings.KAYLEE_WORKER_SCRIPT)
        # I know that this thing does the same, as above,
        # but just for testing purpose... :)
        from kaylee import settings as kl_settings2
        self.assertEqual(Settings1.REGISTRY, kl_settings2.REGISTRY)

    def test_kaylee_setup(self):
        project = DummyProject()
        storage = MemoryControllerResultsStorage()
        app_storage = MemoryProjectResultsStorage()
        controller = DummyController('dummy_app', project, storage, app_storage)
        apps = Applications({'dummy_app' : controller})
        _kl = Kaylee({}, MemoryNodesRegistry(timeout = '2h'), apps)

        from kaylee import kl
        kl._setup(_kl)
        self.assertEqual(kl.applications, _kl.applications)
        self.assertEqual(kl.registry, _kl.registry)

        from kaylee import kl as kl2
        self.assertEqual(kl.applications, _kl.applications)
        self.assertEqual(kl.registry, _kl.registry)

    def test_lazy_settings_setup(self):
        # test setup from a module
        lzs = LazySettings()
        lzs._setup(dummy_settings)
        self.assertEqual(lzs.TEST_OPTION, 'test')


class KayleeTests(KayleeTest):
    def test_register_unregister(self):
        kl = _load(Settings2)
        node_json_config = kl.register('127.0.0.1')
        node_config = json.loads(node_json_config)
        self.assertEqual(len(node_config), 3)
        self.assertIn('node_id', node_config)
        self.assertIn('config', node_config)
        self.assertIn('applications', node_config)

        nid = NodeID(node_id = node_config['node_id'])
        self.assertIn(nid, kl.registry)
        self.assertIn(node_config['node_id'], kl.registry)

        kl.unregister(nid)
        self.assertNotIn(nid, kl.registry)

    def test_subscribe_unsubscribe(self):
        # todo: this should be in test_init()
        # todo: write test_loader and then use Settings to initialize Kaylee here
        kl = _load(Settings2)
        app = kl.applications['dummy.1']
        node_json_config = kl.register('127.0.0.1')
        node_config = json.loads(node_json_config)
        node_id = node_config['node_id']

        # test node.subscribe
        app_json_config = kl.subscribe(node_id, 'dummy.1')
        app_config = json.loads(app_json_config)
        self.assertEqual(app_config['dummy_key'], 'dummy_value')
        node = kl.registry[node_id]
        self.assertEqual(node.controller, app)
        self.assertTrue(0 <= (datetime.now() - node.subscription_timestamp).seconds < 1)

        # test node.unsubscribe
        kl.unsubscribe(node_id)
        self.assertIsNone(node.controller)
        self.assertIsNone(node.subscription_timestamp)
        self.assertIn(node, kl.registry)

kaylee_suite = load_tests([KayleeTests, KayleeLoaderTests])
