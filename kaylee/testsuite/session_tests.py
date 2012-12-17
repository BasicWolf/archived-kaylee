from copy import deepcopy
from kaylee.testsuite import KayleeTest, load_tests
from kaylee.node import Node, NodeID
from kaylee import KayleeError
from kaylee.session import (_encrypt, _decrypt, JSONSessionDataManager,
                            NodeSessionDataManager, PhonySessionDataManager,
                            SESSION_DATA_ATTRIBUTE)

class KayleeSessionTests(KayleeTest):
    def test_encrypt_decrypt(self):
        d1 = {'f1' : 'val1', 'f2' : 20}
        s1 = _encrypt(d1, secret_key='abc')
        d1_d = _decrypt(s1, secret_key='abc')
        self.assertEqual(d1, d1_d)

        # test if incorrect signature raises KayleeError
        s2 = s1[3:] # pad the signature
        self.assertRaises(KayleeError, _decrypt, s2, secret_key='abc')

    def test_node_session_data_manager(self):
        node = Node(NodeID.for_host('127.0.0.1'))
        task = {
            'id' : 'i1',
            '#s1' : 10,
            '#s2' : [1, 2, 3],
        }

        nsdm = NodeSessionDataManager()
        self.assertIsNone(node.session_data)
        nsdm.store(node, task)
        self.assertIsNotNone(node.session_data)

        result = {
            'res' : 'someres',
        }
        nsdm.restore(node, result)
        expected_restored_result = {
            'res' : 'someres',
            '#s1' : 10,
            '#s2' : [1, 2, 3],
        }
        self.assertEqual(result, expected_restored_result)
        self.assertIsNone(node.session_data)


        # test that session is not store in case of no session variables
        task = {
            'id' : 'i2'
        }

        orig_task = deepcopy(task)
        nsdm.store(node, task)
        self.assertIsNone(node.session_data)

        nsdm.restore(node, task)
        self.assertEqual(task, orig_task)


    def test_json_session_data_manager(self):
        node = Node(NodeID.for_host('127.0.0.1'))
        task = {
            'id' : 'i1',
            '#s1' : 10,
            '#s2' : [1, 2, 3],
        }

        jsdm = JSONSessionDataManager(secret_key='abc')
        jsdm.store(node, task)
        self.assertIn(SESSION_DATA_ATTRIBUTE, task)
        self.assertEqual(task['id'], 'i1')
        self.assertNotIn('#s1', task)
        self.assertNotIn('#s2', task)

        result = {
            'res' : 'someres',
            SESSION_DATA_ATTRIBUTE : task[SESSION_DATA_ATTRIBUTE],
        }
        jsdm.restore(node, result)

        expected_restored_result = {
            'res' : 'someres',
            '#s1' : 10,
            '#s2' : [1, 2, 3],
        }
        self.assertEqual(result, expected_restored_result)

        # test that session is not store in case of no session variables
        task = {
            'id' : 'i2'
        }

        orig_task = deepcopy(task)
        jsdm.store(node, task)
        self.assertEqual(task, orig_task)

        jsdm.restore(node, task)
        self.assertEqual(task, orig_task)

    def test_phony_session_data_manager(self):
        node = Node(NodeID.for_host('127.0.0.1'))
        task1 = {
            'id' : 'i1',
            '#s1' : 10,
            '#s2' : [1, 2, 3],
        }

        psdm = PhonySessionDataManager()
        self.assertRaises(KayleeError, psdm.store, node, task1)

        task2 = {
            'id' : 'i1',
        }
        # this should be executed without any errors
        self.assertIsNone(psdm.store(node, task2))


kaylee_suite = load_tests([KayleeSessionTests, ])
