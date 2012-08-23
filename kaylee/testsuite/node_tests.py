import unittest
from datetime import datetime, timedelta
from kaylee import Node, NodeID
from kaylee.errors import InvalidNodeIDError
from kaylee.testsuite import KayleeTest, load_tests


class NodeIDTests(KayleeTest):
    def setUp(self):
        pass

    def test_init(self):
        n1 = NodeID()
        # make sure that NodeID is slot-based object
        self.assertFalse(hasattr(n1, '__dict__'))
        self.assertEqual(len(n1.binary), 10)
        self.assertEqual(len(str(n1)), 20)
        n2 = NodeID(node_id = str(n1))
        self.assertEqual(n1, n2)
        n3 = NodeID(node_id = n1)
        self.assertEqual(n1, n3)

    def test_for_host(self):
        n1 = NodeID.for_host('127.0.0.1')
        self.assertFalse(hasattr(n1, '__dict__'))
        self.assertEqual(len(n1.binary), 10)
        self.assertEqual(len(str(n1)), 20)
        self.assertRaises(TypeError, NodeID.for_host)
        self.assertRaises(TypeError, NodeID.for_host, 1000)
        self.assertRaises(TypeError, NodeID.for_host, 100.1)

    def test_from_object(self):
        n  = NodeID.for_host('127.0.0.1')
        n1 = NodeID.from_object(n)
        self.assertIs(n, n1)
        n2 = NodeID.from_object(str(n))
        self.assertEqual(n, n2)
        node = Node(n)
        n3 = NodeID.from_object(node)
        self.assertEqual(n, n3)
        self.assertRaises(InvalidNodeIDError, NodeID.from_object, 'abc')
        self.assertRaises(TypeError, NodeID.from_object, 10)

    def test_internal_counter(self):
        NodeID._inc = 0 # modified for test purposes only
        remote = '127.0.0.1'
        for i in xrange(0, 2**16 - 1):
            n = NodeID.for_host(remote)
        bid = bytearray(n.binary)
        self.assertEqual(bid[4], 0xFF)
        self.assertEqual(bid[5], 0xFE)

        n = NodeID.for_host(remote)
        bid = bytearray(n.binary)
        self.assertEqual(bid[4], 0x0)
        self.assertEqual(bid[5], 0x0)

    def test_compare(self):
        self.assertLess(NodeID(), NodeID())

    def test_parse(self):
        n1 = NodeID.for_host('127.0.0.1')
        n2 = NodeID(str(n1))
        self.assertEqual(n1, n2)
        n2 = NodeID(unicode(n1))
        self.assertEqual(n1, n2)

        n2 = NodeID(n1)
        self.assertEqual(n1, n2)
        self.assertRaises(TypeError, NodeID, 123)
        self.assertRaises(InvalidNodeIDError, NodeID, 'abc')
        self.assertRaises(InvalidNodeIDError, NodeID, u'1'*10)

    def test_dates(self):
        n1 = NodeID.for_host('127.0.0.1')
        t1 = n1.timestamp
        now = datetime.now()
        self.assertTrue(timedelta(seconds = 0) <= now - t1
                        <= timedelta(seconds = 3))

    def test_hashability(self):
        n1 = NodeID.for_host('127.0.0.1')
        n2 = NodeID(n1)
        d = { n1 : 'abc' }
        self.assertIn(n1, d)
        self.assertIn(n2, d)


class NodeTests(KayleeTest):
    def setUp(self):
        pass

    def test_init(self):
        nid = NodeID.for_host('127.0.0.1')
        node = Node(nid)
        self.assertEqual(nid, node.id)
        self.assertRaises(TypeError, Node, 100)
        self.assertRaises(TypeError, Node, 'abc')

kaylee_suite = load_tests([NodeTests, NodeIDTests, ])
