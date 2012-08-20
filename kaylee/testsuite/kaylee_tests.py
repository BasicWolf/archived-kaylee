# -*- coding: utf-8 -*-
import os
from kaylee.testsuite import KayleeTest, load_tests

import json

from kaylee.contrib import (MemoryTemporalStorage,
                            MemoryPermanentStorage,
                            MemoryNodesRegistry)

from projects.dummy_project.dummy import DummyProject, DummyController

import test_config

from kaylee import NodeID, Node, Kaylee, KayleeError, loader

# from datetime import datetime

class KayleeTests(KayleeTest):
    def test_register_unregister(self):
        kl = loader.load(test_config)
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

    # def test_subscribe_unsubscribe(self):
    #     kl = loader.load(test_config)
    #     app = kl.applications['dummy.1']
    #     node_json_config = kl.register('127.0.0.1')
    #     node_config = json.loads(node_json_config)
    #     node_id = node_config['node_id']

#         # test node.subscribe
#         app_json_config = kl.subscribe(node_id, 'dummy.1')
#         app_config = json.loads(app_json_config)
#         self.assertEqual(app_config['dummy_key'], 'dummy_value')
#         node = kl.registry[node_id]
#         self.assertEqual(node.controller, app)
#         self.assertTrue(0 <= (datetime.now() - node.subscription_timestamp).seconds < 1)

#         # test node.unsubscribe
#         kl.unsubscribe(node_id)
#         self.assertIsNone(node.controller)
#         self.assertIsNone(node.subscription_timestamp)
#         self.assertIn(node, kl.registry)

kaylee_suite = load_tests([KayleeTests])
