# -*- coding: utf-8 -*-
from kaylee.testsuite import KayleeTest, load_tests
from kaylee.storage import TemporalStorage, PermanentStorage
from kaylee.contrib.storages import (MemoryTemporalStorage,
                                     MemoryPermanentStorage)
from copy import deepcopy
from kaylee.node import NodeID

SOME = 10
MANY = 100


def _tgen(i, prefix='t'):
    return "{}{}".format(prefix, i)

def _rgen(i, prefix='r'):
    return "{}{}".format(prefix, i)


class TemporalStorageTestsBase(KayleeTest):
    cls = TemporalStorage

    def setUp(self):
        pass

    def test_init(self):
        ts = self.cls()
        self.assertIsInstance(ts, TemporalStorage)
        self.assertEqual(len(ts), 0)

    def test_add(self):
        # add one
        ts = self.cls()
        node_id = NodeID()
        ts.add('t1', node_id, 'r1')
        self.assertEqual(list(ts['t1']), [(node_id, 'r1'), ])

        # add many
        ts = self.cls()
        node_id = NodeID()
        self._fill_storage(ts, MANY, node_id=node_id)
        for i in range(0, MANY):
            tid = _tgen(i)
            for nid, res in ts[tid]:
                self.assertEqual(nid, node_id)
                self.assertEqual(res, _rgen(i))

    def test_add_complex_result(self):
        ts = self.cls()
        test_res = {
            'edx' : [1, 2, 3],
            'eax' : { (3, 4) : (5, 6), 'c' : 10},
            1 : 100,
            2 : {
                3 : 'abc',
                'cde' : [5, 6, 7] * 100,
                0 : 'c' * 65537
            }
        }
        ts.add('1', NodeID(), deepcopy(test_res))
        nr_list = list(ts['1'])
        added_res = nr_list[0][1]
        self.assertEqual(test_res, added_res)

    def test_overwrite(self):
        # overwrite one
        ts = self.cls()
        node_id = NodeID()
        ts.add('t1', node_id, 'r1')
        ts.add('t1', node_id, 'r2')
        self.assertEqual(list(ts['t1']), [(node_id, 'r2'), ])

        # overwrite many
        ts = self.cls()
        rgen = lambda i : "XYZ{}".format(i)
        self._fill_storage(ts, SOME, node_id=node_id)
        self._fill_storage(ts, SOME, rgen_func=rgen, node_id=node_id)

        for i in range(0, SOME):
            tid = _tgen(i)
            for nid, res in ts[tid]:
                self.assertEqual(nid, node_id)
                self.assertEqual(res, rgen(i))



    def test_remove_and_del(self):
        # remove one
        ts = self.cls()
        node_id = NodeID()
        ts.add('t1', node_id, 'r1')
        ts.remove('t1')
        self.assertRaises(KeyError, ts.__getitem__, 't1')
        self.assertEqual(len(ts), 0)

        # add one, remove two
        ts.add('t1', node_id, 'r1')
        self.assertRaises(KeyError, ts.remove, 't1', NodeID())
        self.assertRaises(KeyError, ts.remove, 't2')
        ts.remove('t1', node_id)
        self.assertEqual(list(ts['t1']), [])
        self.assertEqual(len(ts), 1)
        ts.remove('t1')
        self.assertEqual(len(ts), 0)
        self.assertRaises(KeyError, ts.__getitem__, 't1')

        # test del
        ts.add('t3', node_id, 'r1')
        del ts['t3']
        self.assertRaises(KeyError, ts.__getitem__, 't3')
        self.assertEqual(len(ts), 0)

        # remove many
        ts = self.cls()
        self._fill_storage(ts, SOME, node_id=node_id)
        self.assertEqual(len(ts), SOME)
        for i in range(0, SOME):
            tid = ts[_tgen(i)]
            del ts[_tgen(i)]
            self.assertRaises(KeyError, ts.__getitem__, tid)
        self.assertEqual(len(ts), 0)


    def test_clear(self):
        # fill and clear
        ts = self.cls()
        self._fill_storage(ts, SOME)
        self.assertEqual(len(ts), SOME)
        ts.clear()
        self.assertEqual(len(ts), 0)

        # double fill and clear
        ts = self.cls()
        self._fill_storage(ts, SOME)
        self._fill_storage(ts, SOME)
        self.assertEqual(len(ts), SOME)
        ts.clear()
        self.assertEqual(len(ts), 0)

        # same ts, fill and clear
        self._fill_storage(ts, SOME, node_id=NodeID())
        self.assertEqual(len(ts), SOME)
        ts.clear()
        self.assertEqual(len(ts), 0)

        # remove all and clear
        ts = self.cls()
        self._fill_storage(ts, SOME, node_id=NodeID())
        for i in range(0, SOME):
            ts.remove(_tgen(i))
        self.assertEqual(len(ts), 0)
        ts.clear()
        self.assertEqual(len(ts), 0)


    def test_contains_and_in(self):
        ts = self.cls()
        self._fill_storage(ts, SOME)

        # by task id
        for i in range(0, SOME):
            tid = _tgen(i)
            self.assertTrue(ts.contains(tid))
            self.assertIn(tid, ts)

        self.assertFalse(ts.contains('tx'))
        self.assertNotIn('tx', ts)

        # by node id
        ts = self.cls()
        node_id = NodeID()
        self._fill_storage(ts, SOME, node_id=node_id)
        for i in range(0, SOME):
            tid = _tgen(i)
            self.assertTrue(ts.contains(tid, node_id))
            self.assertFalse(ts.contains(tid, NodeID()))
            self.assertFalse(ts.contains(_tgen(i + SOME), node_id))
            self.assertIn(tid, ts)

        # after clear()
        ts.clear()
        for i in range(0, SOME):
            tid = _tgen(i)
            self.assertFalse(ts.contains(tid))
            self.assertFalse(ts.contains(tid, node_id))
            self.assertNotIn(tid, ts)

    def test_count_and_total_count(self):
        ts = self.cls()
        # test simple amount of stored values
        self._fill_storage(ts, SOME)
        self.assertEqual(len(ts), SOME)
        self.assertEqual(ts.count, SOME)
        self.assertEqual(ts.total_count, SOME)

        # double fill
        self._fill_storage(ts, SOME)
        self._fill_storage(ts, SOME)
        self.assertEqual(len(ts), SOME)
        self.assertEqual(ts.count, SOME)
        self.assertEqual(ts.total_count, 3 * SOME)

        # remove
        ts.remove('t0')
        self.assertEqual(len(ts), SOME - 1)
        self.assertEqual(ts.count, SOME - 1)
        self.assertEqual(ts.total_count, 3 * SOME - 3)

        # remove with specific node id
        nid = NodeID()
        ts.add('t1', nid, 'r12')
        self.assertEqual(len(ts), SOME - 1)
        self.assertEqual(ts.count, SOME - 1)
        self.assertEqual(ts.total_count, 3 * SOME - 2)

        ts.remove('t1', nid)
        self.assertEqual(len(ts), SOME - 1)
        self.assertEqual(ts.count, SOME - 1)
        self.assertEqual(ts.total_count, 3 * SOME - 3)

        # add one, remove
        ts.add('t0', NodeID(), 'r0')
        for i in range(0, SOME):
            ts.remove(_tgen(i))
        self.assertEqual(len(ts), 0)
        self.assertEqual(ts.count, 0)
        self.assertEqual(ts.total_count, 0)

        # more double fill
        self._fill_storage(ts, MANY)
        self._fill_storage(ts, MANY)
        self.assertEqual(len(ts), MANY)
        self.assertEqual(ts.count, MANY)
        self.assertEqual(ts.total_count, 2 * MANY)

        # test nodes count
        nodes = set(n for n, r in ts.values())
        self.assertEqual(len(nodes), 2 * MANY)

    def test_keys_and_iter(self):
        def _basic_ki_test(ts, count):
            test_task_ids = set(_tgen(i) for i in range(0, count))
            iter_task_ids = set(tid for tid in iter(ts))
            keys_task_ids = set(tid for tid in ts.keys())
            self.assertEqual(test_task_ids, iter_task_ids)
            self.assertEqual(test_task_ids, keys_task_ids)
            self.assertEqual(len(iter_task_ids), len(list(iter(ts))))
            self.assertEqual(len(keys_task_ids), len(list(ts.keys())))

        ts = self.cls()
        self._fill_storage(ts, SOME)
        _basic_ki_test(ts, SOME)

        # fill more, same test
        self._fill_storage(ts, SOME)
        _basic_ki_test(ts, SOME)

        # remove a bit
        for i in range(0, SOME):
            ts.remove(_tgen(i))
        _basic_ki_test(ts, 0)

        ts.clear()
        node_id = NodeID()
        self._fill_storage(ts, SOME, node_id=node_id)
        self._fill_storage(ts, SOME)

        for i in range(0, SOME):
            ts.remove(_tgen(i), node_id)
        _basic_ki_test(ts, SOME)

    def test_values(self):
        ts = self.cls()
        self._fill_storage(ts, SOME)
        self.assertEqual(len(list(ts.values())), SOME)

        test_results_set = set(_rgen(i) for i in range(0, SOME))
        for nr in ts.values():
            self.assertIn(nr[1], test_results_set)
            self.assertEqual(NodeID(nr[0]).binary, nr[0])

        # fill once more and count
        self._fill_storage(ts, SOME)
        for nr in ts.values():
            self.assertIn(nr[1], test_results_set)
            self.assertEqual(NodeID(nr[0]).binary, nr[0])
        self.assertEqual(len(list(ts.values())), 2 * SOME)

        # clear and count
        ts.clear()
        self.assertEqual(len(list(ts.values())), 0)

        # specify node id
        node_id = NodeID()
        self._fill_storage(ts, SOME, node_id=node_id)
        for nr in ts.values():
            self.assertIn(nr[1], test_results_set)
            self.assertEqual(NodeID(nr[0]).binary, node_id.binary)

        # remove a result by task_id
        HALF_SOME = SOME // 2
        for i in range(0, HALF_SOME):
            ts.remove(_tgen(i))
        for nr in ts.values():
            res = nr[1]
            self.assertGreaterEqual(int(res[-1]), HALF_SOME)

        # fill more and count
        self._fill_storage(ts, SOME)
        self.assertEqual(len(list(ts.values())), HALF_SOME + SOME)


    @staticmethod
    def _fill_storage(ts, count, tgen_func=_tgen, rgen_func=_rgen, node_id=None):
        if node_id is None:
            # if node_id has not been defined by a user
            # define callable _nodeid == NodeID
            _nodeid = NodeID
        else:
            # a callable which returns the `node_id` argument
            _nodeid = lambda: node_id
        for i in range(0, count):
            ts.add(tgen_func(i), _nodeid(), rgen_func(i))


class PermanentStorageTestsBase(KayleeTest):
    cls = PermanentStorage # redefine in sub-classes

    def setUp(self):
        pass

    def test_init(self):
        ps = self.cls()
        self.assertIsInstance(ps, PermanentStorage)
        self.assertEqual(len(ps), 0)

    def test_add(self):
        ps = self.cls()
        ps.add('1', 'r1')

        self.assertEqual(ps['1'], ['r1'])
        self.assertEqual(len(ps), 1)
        self.assertEqual(list(iter(ps)), ['1'])

        # add many
        ps = self.cls()
        self._fill_storage(ps, MANY)
        self.assertEqual(len(ps), MANY)

        for i in range(0, MANY):
            task_id = _tgen(i)
            result = [_rgen(i)]
            self.assertEqual(ps[task_id], result)

    def test_add_same_task_results(self):
        ps = self.cls()
        self._fill_storage(ps, SOME)
        self._fill_storage(ps, SOME)
        self._fill_storage(ps, SOME)

        for i in range(0, SOME):
            task_id = _tgen(i)
            result = [_rgen(i)] * 3
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

        for i in range(0, SOME):
            ps.add(_tgen(i), deepcopy(res))
            self.assertEqual(ps[_tgen(i)], [res])

    def test_keys_iter(self):
        ps = self.cls()
        self._fill_storage(ps, SOME)
        test_keys_set = set(_tgen(i) for i in range(0, SOME))
        ps_iter_keys_set = set(iter(ps))
        self.assertEqual(len(list(iter(ps))), SOME)
        self.assertEqual(test_keys_set, ps_iter_keys_set)
        self.assertEqual(list(iter(ps)), list(ps.keys()))

    def test_values_iter(self):
        ps = self.cls()
        self._fill_storage(ps, SOME)
        test_values_list = [[_rgen(i)] for i in range(0, SOME)]
        self.assertEqual(test_values_list, sorted(list(ps.values())) )

    def test_count_and_total_count(self):
        ps = self.cls()
        self._fill_storage(ps, SOME)
        self.assertEqual(ps.count, len(ps))
        self.assertEqual(ps.count, SOME)
        self.assertEqual(ps.total_count, SOME)

        ps.add('t0', 'r0')
        self._fill_storage(ps, SOME)
        self.assertEqual(ps.count, SOME)
        self.assertEqual(ps.total_count, SOME * 2 + 1)


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


    @staticmethod
    def _fill_storage(ps, count, tgen_func=_tgen, rgen_func=_rgen):
        for i in range(0, count):
            ps.add(tgen_func(i), _rgen(i))


class MemoryPermanentStorageTests(PermanentStorageTestsBase):
    cls = MemoryPermanentStorage


class MemoryTemporalStorageTests(TemporalStorageTestsBase):
    cls = MemoryTemporalStorage


kaylee_suite = load_tests([
    MemoryTemporalStorageTests,
    MemoryPermanentStorageTests
])
