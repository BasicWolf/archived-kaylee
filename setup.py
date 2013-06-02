#!/usr/bin/env python

import os
from setuptools import setup

import kaylee


def fullsplit(path, result=None):
    """Split a pathname into components (the opposite of os.path.join) in a
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


EXCLUDE_FROM_PACKAGES = [
    'kaylee.manager.commands.templates.project_template',
    'kaylee.testsuite.command_manager_tests_resources.pi_calc',
    'kaylee.testsuite.command_manager_tests_resources.monte_carlo_pi',
]


def is_package(package_name):
    for pkg in EXCLUDE_FROM_PACKAGES:
        if package_name.startswith(pkg):
            return False
    return True

root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
kaylee_dir = 'kaylee'

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, package_data = [], {}

for dirpath, dirnames, filenames in os.walk(kaylee_dir):
    # Ignore PEP 3147 cache dirs and those whose names start with '.'
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
    parts = fullsplit(dirpath)
    package_name = '.'.join(parts)
    if '__init__.py' in filenames and is_package(package_name):
        packages.append(package_name)
    elif filenames:
        relative_path = []
        while '.'.join(parts) not in packages:
            relative_path.append(parts.pop())
        relative_path.reverse()
        path = os.path.join(*relative_path)
        package_files = package_data.setdefault('.'.join(parts), [])
        package_files.extend([os.path.join(path, f) for f in filenames])

setup(
    name='Kaylee',
    version=kaylee.__version__,
    url='http://github.com/basicwolf/kaylee',
    license='LICENSE',
    author='Zaur Nasibov',
    author_email='zaur@znasibov.info',
    description='A distributed and crowd computing framework',
    long_description=open('README').read(),
    packages=packages,
    package_data=package_data,
    zip_safe=False,
    scripts=[
        'kaylee/bin/kaylee-admin.py',
    ],
    install_requires=[
        'Werkzeug>=0.6.1',
        'Jinja2>=2.4',
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
