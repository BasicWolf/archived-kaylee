import os
from kaylee.testsuite import KayleeTest, load_tests, TestSettings
from kaylee import load

class Settings(TestSettings):
    KAYLEE = {
        'nodes_storage' : {
            'name' : 'MemoryNodesStorage',
            'config' : {},
            },
    }

class KayleeLoadTest(KayleeTest):
    def test_load(self):
        kl = load(Settings)

class KayleeTests(KayleeTest):
    def setUp(self):
        self.kl = load(Settings)

kaylee_suite = load_tests([KayleeLoadTest, KayleeTests])
