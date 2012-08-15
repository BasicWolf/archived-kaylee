from setuptools import setup, find_packages

setup(
    name = 'Kaylee',
    version = '0.1dev',
    url = 'http://github.com/basicwolf/kaylee',
    license = 'MIT',
    author = 'Zaur Nasibov',
    author_email = 'zaur@znasibov.info',
    description = 'A distributed and crowd computing framework',
    long_description = open('README.rst').read(),
    packages = ['kaylee', 'kaylee.contrib', 'kaylee.testsuite'],
    scrips = ['kaylee/bin/kaylee-copy-client.py'],
    package_data = {
        'kaylee' : ['client/*.js'],
    },
    zip_safe = False,
    platforms = 'any',
)
