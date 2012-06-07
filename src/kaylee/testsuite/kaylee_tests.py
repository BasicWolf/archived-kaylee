import os
import json

from projects.dummy_project.dummy import DummyProject, DummyController
from kaylee.testsuite import KayleeTest, load_tests, TestSettings
from kaylee import (load, NodeID, Node, Kaylee, KayleeError, Applications, )
from kaylee.loader import load_kaylee_objects
from kaylee.storage import (MemoryNodesStorage, MemoryControllerResultsStorage,
                            MemoryAppResultsStorage)
from datetime import datetime


class Settings1(TestSettings):
    KAYLEE_JS_ROOT = '/path/to/kaylee/js'
    LIB_JS_ROOT    = '/path/to/js/libs'
    PROJECTS_STATIC_ROOT = '/path/to/projects/static'

    NODES_STORAGE = {
        'name' : 'MemoryNodesStorage',
        'config' : {
            'timeout' : '2s',
            },
    }

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

                'results_storage' : {
                    'name' : 'MemoryControllerResultsStorage',
                    'config' : {}
                    },
                'app_results_storage' : {
                    'name' : 'MemoryAppResultsStorage',
                    'config' : {}
                    },
                },
          }
        ]


class KayleeLoaderTests(KayleeTest):
    def test_load_nodes_config(self):
        nconf, storage, apps = load_kaylee_objects(Settings1)
        self.assertEqual(nconf['kaylee_js_root'], Settings1.KAYLEE_JS_ROOT)
        self.assertEqual(nconf['lib_js_root'], Settings1.LIB_JS_ROOT)
        self.assertEqual(nconf['projects_static_root'],
                         Settings1.PROJECTS_STATIC_ROOT)
        self.assertEqual(len(apps), 0)

    def test_load_nodes_storage(self):
        nconf, storage, apps = load_kaylee_objects(Settings1)
        self.assertIsInstance(storage, MemoryNodesStorage)

    def test_load_applications(self):
        nconf, storage, apps = load_kaylee_objects(Settings2)
        self.assertEqual(len(apps), 1)
        app = apps['dummy.1']
        self.assertEqual(app.__class__.__name__, DummyController.__name__)
        self.assertEqual(app.app_name, 'dummy.1')
        self.assertIsInstance(app.results, MemoryControllerResultsStorage)
        self.assertIsInstance(app.app_results, MemoryAppResultsStorage)
        self.assertEqual(app.project.__class__.__name__, DummyProject.__name__)

    def test_load_kaylee(self):
        kl = load(Settings2)
        self.assertIn('dummy.1', kl.applications)
        self.assertIsInstance(kl.nodes, MemoryNodesStorage)

    def test_init_kaylee(self):
        project = DummyProject()
        results_storage = MemoryControllerResultsStorage()
        app_results_storage = MemoryAppResultsStorage()
        controller = DummyController(0, 'dummy_app', project, results_storage,
                                     app_results_storage)
        apps = Applications({'dummy_app' : controller})
        kl = Kaylee({}, MemoryNodesStorage(timeout = '2h'), apps)
        self.assertIn('dummy_app', kl.applications)
        self.assertIsInstance(kl.nodes, MemoryNodesStorage)


class KayleeTests(KayleeTest):
    def test_register_unregister(self):
        kl = load(Settings2)
        node_json_config = kl.register('127.0.0.1')
        node_config = json.loads(node_json_config)
        self.assertEqual(len(node_config), 3)
        self.assertIn('node_id', node_config)
        self.assertIn('config', node_config)
        self.assertIn('applications', node_config)

        nid = NodeID(node_id = node_config['node_id'])
        self.assertIn(nid, kl.nodes)
        self.assertIn(node_config['node_id'], kl.nodes)

        kl.unregister(nid)
        self.assertNotIn(nid, kl.nodes)

    def test_subscribe_unsubscribe(self):
        # todo: this should be in test_init()
        # todo: write test_loader and then use Settings to initialize Kaylee here
        kl = load(Settings2)
        app = kl.applications['dummy.1']
        node_json_config = kl.register('127.0.0.1')
        node_config = json.loads(node_json_config)
        node_id = node_config['node_id']

        # test node.subscribe
        app_json_config = kl.subscribe(node_id, 'dummy.1')
        app_config = json.loads(app_json_config)
        self.assertEqual(app_config['dummy_key'], 'dummy_value')
        node = kl.nodes[node_id]
        self.assertEqual(node.controller, app)
        self.assertTrue(0 <= (datetime.now() - node.subscription_timestamp).seconds < 1)

        # test node.unsubscribe
        kl.unsubscribe(node_id)
        self.assertIsNone(node.controller)
        self.assertIsNone(node.subscription_timestamp)
        self.assertIn(node, kl.nodes)

kaylee_suite = load_tests([KayleeTests, KayleeLoaderTests])
