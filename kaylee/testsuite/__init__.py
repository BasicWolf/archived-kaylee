# -*- coding: utf-8 -*-
import os
import sys
import unittest
from importlib import import_module

unittest.defaultTestLoader = unittest.TestLoader()

PROJECTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'projects')
sys.path.insert(0, PROJECTS_DIR)

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
    sys.path.insert(0, cdir)
    for fname in os.listdir(cdir):
        if not fname.endswith('_tests.py'):
            continue
        modname = fname[:-3]
        mod = import_module(modname)
        if hasattr(mod, 'kaylee_suite'):
            suite.addTest(mod.kaylee_suite)
    return suite


def find_all_tests(root_suite):
    """Yields all the tests and their names from a given suite."""
    suites = [root_suite]
    while suites:
        suite = suites.pop()
        try:
            # not that suite is iterable, thus every sub-suite from suite
            # is appended to the suites list
            suites.extend(suite)
        except TypeError:
            yield suite, '{}.{}.{}'.format(
                suite.__class__.__module__,
                suite.__class__.__name__,
                suite._testMethodName ).lower()


class KayleeTestsLoader(unittest.TestLoader):
    """
    A custom loader for Kaylee unit tests.
    Usage example:
    1. test.py kaylee_tests   # loads the suite from the module
    2. test.py KayleeLoadTest # loads particular TestCase
    3. test.py test_settings  # loads all(!) test functions with that name
    4. test.py KayleeLoadTest.test_settings # loads test function from TestCase
    5. test.py kaylee_tests.KayleeLoadTest, same as (2).
    """

    def __init__(self):
        self._default_suite = suite()

    def loadTestsFromName(self, name, module = None):
        name = name.lower()
        if name == 'default':
            return self._default_suite

        tests = []
        for testcase, testname in find_all_tests(self._default_suite):
            if (testname == name or
                testname.endswith('.' + name) or
                ('.' + name + '.') in testname or
                testname.startswith(name + '.') ):
                tests.append(testcase)

        if not tests:
            raise LookupError('Could not find test case for "{}"'.format(name))

        suite = unittest.TestSuite()
        if len(tests) == 1:
            return tests[0]
        for test in tests:
            suite.addTest(test)
        return suite


def main():
    """Runs the testsuite as command line application."""
    unittest.main(testLoader = KayleeTestsLoader(), defaultTest = 'default')
