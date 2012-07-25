from kaylee.testsuite import KayleeTest, load_tests
from kaylee.util import parse_timedelta, LazyObject
from kaylee import KayleeError

class KayleeUtilTests(KayleeTest):
    def test_parse_timedelta(self):
        t1 = parse_timedelta('2d')
        self.assertEqual(t1.days, 2)
        self.assertEqual(t1.seconds, 0)
        self.assertEqual(t1.microseconds, 0)

        t2 = parse_timedelta('2d 1h')
        self.assertEqual(t2.days, 2)
        self.assertEqual(t2.seconds, 3600)

        t3 = parse_timedelta('1h 10m 10s')
        self.assertEqual(t3.days, 0)
        self.assertEqual(t3.seconds, 4210)
        self.assertEqual(t3.microseconds, 0)

        t4 = parse_timedelta('25h 10s')
        self.assertEqual(t4.days, 1)
        self.assertEqual(t4.seconds, 3610)

        t5 = parse_timedelta('2d 1x')
        self.assertEqual(t5.days, 2)
        self.assertEqual(t5.seconds, 0)

        self.assertRaises(KayleeError, parse_timedelta, '25x 10x')

    def test_lazy_object(self):
        class NonLazy(object):
            def __init__(self):
                self._x = 10
                self.y = 20

            @property
            def x(self):
                return self._x

            @x.setter
            def x(self, val):
                self._x = val

            def x_plus(self, val):
                self.x += val


        class MyLazyObject(LazyObject):
            def _setup(self, obj = None):
                self._wrapped = NonLazy() if obj is None else obj

        lo = MyLazyObject()
        self.assertIsNone(lo._wrapped)
        lo.y = 20
        self.assertIsNotNone(lo._wrapped)
        self.assertEqual(lo.y, 20)
        self.assertEqual(lo.x, 10)
        lo.x_plus(40)
        self.assertEqual(lo.x, 50)

kaylee_suite = load_tests([KayleeUtilTests, ])
