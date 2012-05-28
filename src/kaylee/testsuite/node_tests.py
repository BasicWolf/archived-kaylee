import unittest
from datetime import datetime, timedelta
from kaylee import Node, NodeID
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
        self.assertEqual(len(str(n1)), 20)

    def test_internal_counter(self):
        NodeID._inc = 0 # modified only for test purposes
        remote = '127.0.0.1'
        for i in xrange(0, 2**16 - 1):
            n = NodeID(remote)
        bid = bytearray(n.binary)
        self.assertEqual(bid[8], 0xFF)
        self.assertEqual(bid[9], 0xFE)

        n = NodeID(remote)
        bid = bytearray(n.binary)
        self.assertEqual(bid[8], 0x0)
        self.assertEqual(bid[9], 0x0)

    def test_parse(self):
        n1 = NodeID('127.0.0.1')
        n2 = NodeID(node_id = str(n1))
        self.assertEqual(n1, n2)
        n2 = NodeID(node_id = unicode(n1))
        self.assertEqual(n1, n2)

        n2 = NodeID(node_id = n1)
        self.assertEqual(n1, n2)
        self.assertRaises(TypeError, NodeID, node_id = 123)
        self.assertRaises(InvalidNodeIDError, NodeID, node_id = 'abc')
        self.assertRaises(InvalidNodeIDError, NodeID, node_id = u'1'*10)

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


class NodeTests(KayleeTest):
    def setUp(self):
        pass

    def test_init(self):
        nid = NodeID('127.0.0.1')
        node = Node(nid)
        self.assertEqual(nid, node.id)
        self.assertRaises(TypeError, Node, 100)
        self.assertRaises(TypeError, Node, 'abc')

kaylee_suite = load_tests([NodeTests, NodeIDTests, ])
