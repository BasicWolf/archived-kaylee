from copy import deepcopy
from kaylee.testsuite import KayleeTest, load_tests
from kaylee.node import Node, NodeID
from kaylee import KayleeError
from kaylee.session import (_encrypt, _decrypt, ClientSessionDataManager,
                            ServerSessionDataManager, PhonySessionDataManager,
                            SESSION_DATA_ATTRIBUTE, EncryptedSessionDataManager,
                            SessionDataManager,)
from kaylee.errors import SessionKeyNameError

class KayleeSessionTests(KayleeTest):
    def test_encrypt_decrypt(self):
        # a dict
        d1 = {'#f1' : 'val1', '#f2' : 20}
        s1 = _encrypt(d1, 'abc')
        d1_d = _decrypt(s1, 'abc')
        self.assertEqual(d1, d1_d)

        # test if incorrect signature raises KayleeError
        s2 = s1[3:] # pad the signature
        self.assertRaises(KayleeError, _decrypt, s2, 'abc')

        # a list
        d3 = ['123', 123, {1, 2, 3}]
        s3 = _encrypt(d3, 'abc')
        d3_d = _decrypt(s3, 'abc')
        self.assertEqual(d3, d3_d)

        # an int
        d4 = 123
        s4 = _encrypt(d4, 'abc')
        d4_d = _decrypt(s4, 'abc')
        self.assertEqual(d4, d4_d)

    def test_session_errors(self):
        # test for unicode characters in encrypted data
        derr = [
            {'#я1' : 'val1', '#f2' : 20},
            {'#s1' : 'val1', '#ц2' : 20},
        ]
        for d in derr:
            self.assertRaises(SessionKeyNameError, SessionDataManager.get_session_data, d)

    def test_node_session_data_manager(self):
        node = Node(NodeID.for_host('127.0.0.1'))
        task = {
            'id' : 'i1',
            '#s1' : 10,
            '#s2' : [1, 2, 3],
        }

        nsdm = ServerSessionDataManager()
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

        jsdm = ClientSessionDataManager(secret_key='abc')
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

        jsdm2 = ClientSessionDataManager(secret_key='abc')
        self.assertIsInstance(jsdm2, EncryptedSessionDataManager)
        self.assertEqual(len(jsdm2.secret_key), (len('abc')))

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

    def test_is_abstract(self):
        self.assertRaises(TypeError, SessionDataManager)

kaylee_suite = load_tests([KayleeSessionTests, ])
