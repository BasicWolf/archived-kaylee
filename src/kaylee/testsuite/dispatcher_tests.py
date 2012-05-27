import os
from kaylee.testsuite import KayleeTest, load_tests, TestSettings
from kaylee import load

class Settings(TestSettings):
    DISPATCHER = {
        'nodes_storage' : {
            'name' : 'MemoryNodesStorage',
            'config' : {},
            },
    }

class DispatcherLoadTest(KayleeTest):    
    def test_load(self):
        kl = load(Settings)

class DispatcherTests(KayleeTest):
    def setUp(self):
        self.kl = load(Settings)    

kaylee_suite = load_tests([DispatcherLoadTest, DispatcherTests])
