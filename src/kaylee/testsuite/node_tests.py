import os
from kaylee.testsuite import KayleeTest, load_tests
from kaylee import Node, NodeID, load

class NodeTests(KayleeTest):    
    def setUp(self):
        pass


kaylee_suite = load_tests([NodeTests])
