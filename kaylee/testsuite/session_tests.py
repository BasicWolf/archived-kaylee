import string
from kaylee.testsuite import KayleeTest, load_tests
from kaylee import KayleeError
from kaylee.session import _encrypt, _decrypt

class KayleeSessionTests(KayleeTest):
    def test_encrypt_decrypt(self):
        d1 = {'f1' : 'val1', 'f2' : 20}
        s1 = _encrypt(d1, secret_key='abc')
        d1_d = _decrypt(s1, secret_key='abc')
        self.assertEqual(d1, d1_d)

        # test if incorrect signature raises KayleeError
        s2 = s1[3:] # pad the signature
        self.assertRaises(KayleeError, _decrypt, s2, secret_key='abc')


kaylee_suite = load_tests([KayleeSessionTests, ])
