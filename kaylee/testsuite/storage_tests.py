from kaylee.testsuite import KayleeTest, load_tests
from kaylee.storage import TemporalStorage, PermanentStorage
from kaylee.contrib.storages import (MemoryTemporalStorage,
                                     MemoryPermanentStorage)
from copy import deepcopy

SOME = 10
MANY = 100

class PermanentStorageTestsBase(KayleeTest):
    cls = PermanentStorage # redefine in sub-classes

    def setUp(self):
        pass

    def test_init(self):
        ps = self.cls()
        self.assertEqual(len(ps), 0)

    def test_add_one(self):
        ps = self.cls()
        ps.add('1', 'r1')

        self.assertEqual(ps['1'], ['r1'])
        self.assertEqual(len(ps), 1)
        self.assertEqual(list(iter(ps)), ['1'])

    def test_add_many(self):
        ps = self.cls()
        self._fill_storage(ps, MANY)
        self.assertEqual(len(ps), MANY)

        for i in range(0, MANY):
            task_id = self._tid(i)
            result = [self._rid(i)]
            self.assertEqual(ps[task_id], result)

    def test_add_same_task_results(self):
        ps = self.cls()
        self._fill_storage(ps, SOME)
        self._fill_storage(ps, SOME)
        self._fill_storage(ps, SOME)

        for i in range(0, SOME):
            task_id = self._tid(i)
            result = [self._rid(i)] * 3
            self.assertEqual(ps[task_id], result)

    def test_add_complex_result(self):
        ps = self.cls()
        res = {
            'edx' : [1, 2, 3],
            'eax' : { (3, 4) : (5, 6), 'c' : 10},
            1 : 100,
            2 : {
                3 : 'abc',
                'cde' : [5, 6, 7] * 100,
                0 : 'c' * 65537
            }
        }
        ps.add('1', deepcopy(res))
        self.assertEqual(ps['1'], [res, ])

        ps.add('1', deepcopy(res))
        self.assertEqual(ps['1'], [res, res])


    def test_keys_iter(self):
        ps = self.cls()
        self._fill_storage(ps, SOME)
        test_keys_set = set(self._tid(i) for i in range(0, SOME))
        ps_iter_keys_set = set(iter(ps))
        self.assertEqual(len(list(iter(ps))), SOME)
        self.assertEqual(test_keys_set, ps_iter_keys_set)
        self.assertEqual(list(iter(ps)), list(ps.keys()))

    def test_values_iter(self):
        ps = self.cls()
        self._fill_storage(ps, SOME)
        test_values_list = [[self._rid(i)] for i in range(0, SOME)]
        self.assertEqual(test_values_list, sorted(list(ps.values())) )

    def test_count(self):
        ps = self.cls()
        self._fill_storage(ps, SOME)
        self.assertEqual(ps.count, SOME)
        self.assertEqual(ps.count, len(ps))

    def test_total_count(self):
        ps = self.cls()
        self._fill_storage(ps, SOME)
        self._fill_storage(ps, SOME)
        self.assertEqual(ps.total_count, SOME * 2)

    def test_contains(self):
        ps = self.cls()
        self._fill_storage(ps, SOME)
        self.assertTrue(ps.contains('t0'))
        self.assertTrue(ps.contains("t{}".format(SOME - 1)))
        self.assertIn('t0', ps)
        self.assertIn("t{}".format(SOME - 1), ps)
        self.assertIn("t{}".format(SOME // 2), ps)
        self.assertFalse(ps.contains('xx'))
        self.assertNotIn('xx', ps)
        self.assertTrue(ps.contains('t0', 'r0'))
        self.assertTrue(ps.contains("t{}".format(SOME - 1),
                                    "r{}".format(SOME - 1)) )
        self.assertFalse(ps.contains('t0', 'aa'))

        ps.add('t0', 'abc')
        self.assertTrue(ps.contains('t0', 'abc'))
        self.assertTrue(ps.contains('t0', 'r0'))

        for i in range(0, MANY):
            res = "{}{}".format('n', i)
            ps.add('t0', res)
            self.assertTrue(ps.contains('t0', res))


    def _fill_storage(self, ps, count, tid_prefix='t', res_prefix='r'):
        for i in range(0, count):
            ps.add("{}{}".format(tid_prefix, i), "{}{}".format(res_prefix, i))

    def _tid(self, i, prefix='t'):
        return "{}{}".format(prefix, i)

    def _rid(self, i, prefix='r'):
        return "{}{}".format(prefix, i)


class MemoryPermanentStorageTests(PermanentStorageTestsBase):
    cls = MemoryPermanentStorage


kaylee_suite = load_tests([MemoryPermanentStorageTests])
