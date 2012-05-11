import unittest
from datetime import datetime, timedelta
from kaylee import NodeID
from kaylee.errors import InvalidNodeIDError
from kaylee.tz_util import utc

class NodeIDTests(unittest.TestCase):
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
        n2 = NodeID(nid = str(n1))
        self.assertEqual(n1, n2)
        n3 = NodeID(nid = n2)
        self.assertEqual(n2, n3)
        self.assertRaises(TypeError, NodeID, nid = 123)
        self.assertRaises(InvalidNodeIDError, NodeID, nid = 'abc')

    def test_dates(self):
        n1 = NodeID('127.0.0.1')
        t1 = n1.generation_time
        utcnow = datetime.now(utc)
        self.assertTrue(utcnow - t1 <= timedelta(seconds = 1))
