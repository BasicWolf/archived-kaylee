import unittest
from datetime import datetime, timedelta
from kaylee import NodeID
from kaylee.errors import InvalidNodeIDError
from kaylee.tz_util import utc
from kaylee.testsuite import KayleeTest, load_tests

class NodeIDTests(KayleeTest):
    def setUp(self):
        pass

    def test_init(self):
        n1 = NodeID('127.0.0.1')
        # make sure that NodeID is slot-based object
        self.assertFalse(hasattr(n1, '__dict__'))
        self.assertEqual(len(n1.binary), 10)
        self.assertRaises(TypeError, NodeID)
        self.assertRaises(TypeError, NodeID, 1000)
        self.assertRaises(TypeError, NodeID, 100.1)

    def test_parse(self):
        n1 = NodeID('127.0.0.1')
        n2 = NodeID(node_id = str(n1))
        self.assertEqual(n1, n2)
        n3 = NodeID(node_id = n2)
        self.assertEqual(n2, n3)
        self.assertRaises(TypeError, NodeID, node_id = 123)
        self.assertRaises(InvalidNodeIDError, NodeID, node_id = 'abc')

    def test_dates(self):
        n1 = NodeID('127.0.0.1')
        t1 = n1.generation_time
        utcnow = datetime.now(utc)
        self.assertTrue(utcnow - t1 <= timedelta(seconds = 1))

    def test_hashability(self):
        n1 = NodeID('127.0.0.1')
        n2 = NodeID(node_id = n1)
        d = { n1 : 'abc' }
        self.assertIn(n1, d)
        self.assertIn(n2, d)


kaylee_suite = load_tests([NodeIDTests, ])