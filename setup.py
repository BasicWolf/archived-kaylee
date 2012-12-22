#!/usr/bin/env python

import os
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
from setuptools import setup, find_packages

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils not to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)

packages = []

for dirpath, dirnames, filenames in os.walk('kaylee'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    # elif filenames:
        # data_files.append([dirpath, [os.path.join(dirpath, f)
        #                              for f in filenames]])

data_files = [
    ('kaylee/client', ['kaylee/client/kaylee.js',
                       'kaylee/client/klworker.js']),
]

setup(
    name = 'Kaylee',
    version = '0.2',
    url = 'http://github.com/basicwolf/kaylee',
    license = 'LICENSE',
    author = 'Zaur Nasibov',
    author_email = 'zaur@znasibov.info',
    description = 'A distributed and crowd computing framework',
    long_description = open('README').read(),
    packages = packages,
    data_files = data_files,
    scripts = ['kaylee/bin/kaylee-copy-client.py'],
    zip_safe = False,
    platforms = 'any',
    install_requires=[
        'pycrypto>=2.6',
    ],

    test_suite='kaylee.testsuite.suite',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: JavaScript',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
    ],
)
