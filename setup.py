#!/usr/bin/env python

import sys
from setuptools import setup, find_packages


if sys.version_info < (3, 5, 0):
    sys.stderr.write('ERROR: You need Python 3.5+ to install the typing package.\n')
    exit(1)


def _read_readme():
    with open('./README.md', 'r') as f:
        return f.read()


metadata = {
    'name':             'dicon',
    'version':          '0.0.1',
    'description':      'Dicon, simple DI container injection liblary for Python.',
    'long_description': _read_readme(),
    'url':              'https://github.dena.jp/kenoss/dicon',
    'author':           'keno',
    'author_email':     'keno.ss57@gmail.com',
    'license':          'MIT',
    'packages':         find_packages('src'),
    'package_dir':      {'': 'src'},
    'test_suite':       'tests',
    'install_requires': [],
    'tests_require':    [],
    'setup_requires':   [],
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ]
}
setup(**metadata)
