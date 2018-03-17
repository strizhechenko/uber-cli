#!/usr/bin/env python

"""The setup and build script for the netutils-linux."""

import os
import setuptools


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setuptools.setup(
    name='uber-cli',
    version='1.0.0',
    author='Oleg Strizhechenko',
    author_email='oleg.strizhechenko@gmail.com',
    license='MIT',
    url='https://github.com/strizhechenko/uber-cli',
    keywords='uber cli rides taxi util',
    description='Unofficial read-only Uber CLI on top of uber-rides.',
    packages=['uber_cli'],
    entry_points={
        'console_scripts': [
            'uber-cli=uber_cli.__init__:main',
        ],
    },
    install_requires=['pyyaml', 'uber-rides', 'pygeocoder'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
)
