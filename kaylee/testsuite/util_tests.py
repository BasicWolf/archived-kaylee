import string
from kaylee.testsuite import KayleeTest, load_tests
from kaylee.util import (parse_timedelta, LazyObject, random_string, encrypt,
                         decrypt, get_secret_key)
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


    def test_random_string(self):
        # test length
        s = random_string(5)
        self.assertEqual(len(s), 5)
        s = random_string(0)
        self.assertEqual(len(s), 0)
        s = random_string(100)
        self.assertEqual(len(s), 100)

        # test 'alphabet' argument
        s = random_string(10, 'a')
        self.assertEqual(s, 'a'*10)

        # test other arguments
        s = random_string(30, uppercase=False, lowercase=False)
        for c in s:
            self.assertIn(c, string.digits)

        s = random_string(30, lowercase=False, digits=False)
        for c in s:
            self.assertIn(c, string.ascii_uppercase)

        s = random_string(30, uppercase=False, digits=False)
        for c in s:
            self.assertIn(c, string.ascii_lowercase)

        # test 'extra' argument
        s = random_string(30, uppercase=False, lowercase=False, digits=False,
                          extra='123')
        for c in s:
            self.assertIn(c, '123')

        extra = '1234567890'
        s = random_string(1000, uppercase=False, digits=False, extra=extra)
        for c in s:
            self.assertIn(c, string.ascii_lowercase + extra)

    def test_get_secret_key(self):
        sk = get_secret_key('abc')
        self.assertEqual(sk, 'abc')

        # test when config is not loaded
        self.assertRaises(KayleeError, get_secret_key)

        # test loading from config
        import test_config
        from kaylee import kl, setup
        setup(test_config)
        sk = get_secret_key()
        self.assertEqual(sk, test_config.SECRET_KEY)

        # test if default parameter works after previous call
        sk = get_secret_key('abc')
        self.assertEqual(sk, 'abc')

        # test for proper behaviour after releasing the object from proxy
        setup(None)
        self.assertRaises(KayleeError, get_secret_key)

        # and the final test :)
        sk = get_secret_key('abc')
        self.assertEqual(sk, 'abc')

    def test_encrypt_decrypt(self):
        d1 = {'f1' : 'val1', 'f2' : 20}
        s1 = encrypt(d1, secret_key='abc')
        d1_d = decrypt(s1, secret_key='abc')
        self.assertEqual(d1, d1_d)

        # test if incorrect signature raises KayleeError
        s2 = s1[3:] # pad the signature
        self.assertRaises(KayleeError, decrypt, s1)


kaylee_suite = load_tests([KayleeUtilTests, ])
