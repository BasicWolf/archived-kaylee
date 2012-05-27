import os
from kaylee.testsuite import KayleeTest, 
from kaylee import Node, NodeID

class NodeTests(KayleeTest):    
    def test_load(self):
        kl = load(Settings)

class DispatcherTests(KayleeTest):
    def setUp(self):
        self.kl = load(Settings)    

kaylee_suite = load_tests([DispatcherLoadTest, DispatcherTests])
