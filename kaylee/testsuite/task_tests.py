import unittest
import kaylee
from kaylee.testsuite import KayleeTest, load_tests
from kaylee.errors import KayleeError

class TaskSimpleFields(kaylee.Task):
    serializable = ['f1', 'f2']

    def __init__(self, task_id, f1, f2):
        super(TaskSimpleFields, self).__init__(task_id)
        self.f1 = f1
        self.f2 = f2


class TaskSessionFields(kaylee.Task):
    serializable = ['#f1', '#f2']

    def __init__(self, task_id, f1, f2):
        super(TaskSessionFields, self).__init__(task_id)
        self.f1 = f1
        self.f2 = f2


class TaskTests(KayleeTest):
    def setUp(self):
        pass

    def test_simple_serialize(self):
        t1 = TaskSimpleFields(1, 10, 'someval')
        d = t1.serialize()
        self.assertEqual(d['id'], '1')
        self.assertEqual(d['f1'], 10)
        self.assertEqual(d['f2'], 'someval')

    def test_secret_key_config_check(self):
        # Checks if KayleeError raised when SECRET_KEY is not defined
        import test_config
        from kaylee import setup, kl
        secret_key = test_config.SECRET_KEY

        del test_config.SECRET_KEY
        setup(test_config)

        t1 = TaskSessionFields(1, 10, 'someval')
        self.assertRaises(KayleeError, t1.serialize)

    def test_session_serialize(self):
        import test_config
        from kaylee import setup, kl
        setup(test_config)

        t1 = TaskSessionFields(1, 10, 'someval')
        d = t1.serialize()
        self.assertIn('__kaylee_task_session__', d)
        val = d['__kaylee_task_session__']
        self.assertGreater(len(val), 0)
        self.assertEqual(val.count('&'), 2)

    def test_session_deserialize(self):
        import test_config
        from kaylee import setup, kl
        setup(test_config)

        t1 = TaskSessionFields(1, 10, 'someval')
        d1 = t1.serialize()

        # check if deserialization works in general
        d2 = TaskSessionFields.deserialize(d1)
        self.assertEqual(len(d2), 3)
        self.assertEqual(d2['f1'], t1.f1)
        self.assertEqual(d2['f2'], t1.f2)
        self.assertEqual(d2['id'], t1.id)

        # test if deserialization works for a string
        s = d1['__kaylee_task_session__']
        d3 = TaskSessionFields.deserialize(s)
        self.assertEqual(len(d3), 2)
        self.assertEqual(d3['f1'], t1.f1)
        self.assertEqual(d3['f2'], t1.f2)
        self.assertNotIn('id', d3)

        # test if incorrect signature raises KayleeError
        s2 = s
        s2 = s[3:] # pad the signature
        self.assertRaises(KayleeError, TaskSessionFields.deserialize, s2)

kaylee_suite = load_tests([TaskTests])
