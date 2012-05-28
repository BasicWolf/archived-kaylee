import os
import json

from kaylee.testsuite import KayleeTest, load_tests, TestSettings
from kaylee import load, NodeID, Node
from kaylee.storage import MemoryNodesStorage


class Settings(TestSettings):
    KAYLEE = {
        'nodes_storage' : {
            'name' : 'MemoryNodesStorage',
            'config' : {},
            },
    }

class KayleeLoadTest(KayleeTest):
    def test_load(self):
        kl = load(Settings)

class KayleeTests(KayleeTest):
    def setUp(self):
        self.kl = load(Settings)

    def test_settings(self):
        self.assertIsInstance(self.kl.nodes, MemoryNodesStorage)

    def test_register(self):
        sreg = self.kl.register('127.0.0.1')
        reg = json.loads(sreg)
        self.assertEqual(len(reg), 2)
        self.assertIn('node_id', reg)

        nid = NodeID(node_id = reg['node_id'])
        self.assertIn(nid, self.kl.nodes)


kaylee_suite = load_tests([KayleeLoadTest, KayleeTests])
