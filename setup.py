#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pylocatereader',
    version='0.1.0',
    description="Locate implementation with extra filtering features, compatible with mlocate.db format.",
    long_description=readme + '\n\n' + history,
    author="Aetf",
    author_email='aetf@unlimitedcodeworks.xyz',
    url='https://github.com/aetf/pylocatereader',
    packages=[
        'pylocatereader',
    ],
    package_dir={'pylocatereader':
                 'pylocatereader'},
    entry_points={
        'console_scripts': [
            'pylocatereader=pylocatereader.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='pylocatereader',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
