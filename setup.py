#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'sqlflow'
DESCRIPTION = 'SQLFlow client library for Python.'
URL = 'https://github.com/sql-machine-learning/sqlflow'
EMAIL = 'kuisong.tong@gmail.com'
AUTHOR = 'Kuisong Tong'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    'protobuf >=3.6, <4',
    'grpcio >=1.17, <2',
    'ipython>=1.0',
    'prettytable',
]
SETUP_REQUIRED = [
    'pytest-runner'
]
TEST_REQUIRED = [
    'pytest',
]

# What packages are optional?
EXTRAS = {
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's _version.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '_version.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    package_data={'sqlflow': ['proto/*.py']},
    entry_points={
        'console_scripts': ['sqlflow = sqlflow.__main__:main'],
    },
    install_requires=REQUIRED,
    setup_requires=SETUP_REQUIRED,
    tests_require=TEST_REQUIRED,
    extras_require=EXTRAS,
    license='Apache License 2.0',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
