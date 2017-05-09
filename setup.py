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
    version='0.0.1',
    author='Oleg Strizhechenko',
    author_email='oleg.strizhechenko@gmail.com',
    license='MIT',
    url='https://github.com/strizhechenko/netutils-linux',
    keywords='uber cli rides taxi util',
    description='Unofficial read-only Uber CLI on top of uber-rides.',
    packages=setuptools.find_packages(exclude=['tests*']),
    scripts=[os.path.join('utils/', script) for script in os.listdir('utils/')],
    install_requires=['pyyaml', 'uber-rides', 'pygeocoder'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
)
