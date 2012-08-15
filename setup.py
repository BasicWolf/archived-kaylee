from setuptools import setup, find_packages

setup(
    name = 'Kaylee',
    version = '0.1dev',
    url = 'http://github.com/basicwolf/kaylee',
    license='MIT',
    author='Zaur Nasibov',
    author_email='zaur@znasibov.info',
    description='A distributed and crowd computing framework',
    long_description=open('README.rst').read(),
    packages= ['kaylee'],
    zip_safe=False,
    platforms='any',
)
