from setuptools import setup, find_packages

version = __import__('kaylee').get_version()

setup(
    name = 'Kaylee',
    version = version,
    url = 'http://github.com/basicwolf/kaylee',
    license = 'MIT',
    author = 'Zaur Nasibov',
    author_email = 'zaur@znasibov.info',
    description = 'A distributed and crowd computing framework',
    long_description = open('README.rst').read(),
    packages = ['kaylee', 'kaylee.contrib', 'kaylee.testsuite'],
    scripts = ['kaylee/bin/kaylee-copy-client.py'],
    zip_safe = False,
    platforms = 'any',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: JavaScript',
        'Programming Language :: CoffeeScript',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
    ],
)
