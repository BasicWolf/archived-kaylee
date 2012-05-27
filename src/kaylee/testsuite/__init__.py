# -*- coding: utf-8 -*-
import os
import unittest
from importlib import import_module

unittest.defaultTestLoader = unittest.TestLoader()

class TestSettings(object):
    """A simple object wrapper which emulates Kaylee settings module
    in tests."""
    PROJECTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'projects')
    APPLICATIONS = []


def load_tests(test_cases):
    suite = unittest.TestSuite()
    for tcase in test_cases:
        loaded_suite = unittest.defaultTestLoader.loadTestsFromTestCase(tcase)
        suite.addTest(loaded_suite)
    return suite

class KayleeTest(unittest.TestCase):
    """Base class for all Kaylee tests."""


def suite():
    """A testsuite that has all Kaylee tests.  You can use this
    function to integrate Kaylee tests into your own testsuite
    in case you want to test that monkeypatches to Kaylee do not
    break it.
    """
    suite = unittest.TestSuite()
    cdir = os.path.dirname(os.path.abspath(__file__))
    for fname in os.listdir(cdir):
        if not fname.endswith('.py'):
            continue
        modname = fname[:-3]
        mod = import_module(modname)
        if hasattr(mod, 'kaylee_suite'):
            suite.addTest(mod.kaylee_suite)
    return suite


class KayleeTestsLoader(unittest.TestLoader):
    def __init__(self):
        self._default_suite = suite()

    def loadTestsFromName(self, name, module = None):        
        if name == 'default':
            return self._default_suite

def main():
    """Runs the testsuite as command line application."""
    unittest.main(testLoader = KayleeTestsLoader(), defaultTest = 'default')
