import os
import json

from kaylee.testsuite import KayleeTest, load_tests, TestSettings
from kaylee import load, NodeID, Node, Kaylee, KayleeError
from kaylee.storage import MemoryNodesStorage

class Settings_0(TestSettings):
    pass

class Settings_1(TestSettings):
    KAYLEE = {
        'nodes_storage' : {
            'name' : 'MemoryNodesStorage',
            'config' : {},
            },
    }


class KayleeLoaderTests(KayleeTest):
    def test_loader(self):
        self.assertRaises(KayleeError, load, Settings_0)
        kl = load(Settings_1)
        self.assertIsInstance(kl.nodes, MemoryNodesStorage)


class KayleeTests(KayleeTest):
    def test_register_unregister(self):
        kl = Kaylee(MemoryNodesStorage())
        sreg = kl.register('127.0.0.1')
        reg = json.loads(sreg)
        self.assertEqual(len(reg), 2)
        self.assertIn('node_id', reg)

        nid = NodeID(node_id = reg['node_id'])
        self.assertIn(nid, kl.nodes)
        self.assertIn(reg['node_id'], kl.nodes)

        kl.unregister(nid)
        self.assertNotIn(nid, kl.nodes)


kaylee_suite = load_tests([KayleeLoaderTests, KayleeTests])
