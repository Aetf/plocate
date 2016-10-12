#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

parsed_requirements = parse_requirements(
    'requirements/prod.txt',
    session=PipSession()
)
requirements = [str(ir.req) for ir in parsed_requirements]

parsed_test_requirements = parse_requirements(
    'requirements/test.txt',
    session=PipSession()
)
test_requirements = [str(tr.req) for tr in parsed_test_requirements]

setup(
    name='plocate',
    version='0.1.2',
    description="Locate implementation with extra filtering features, compatible with mlocate.db format.",
    long_description=readme + '\n\n' + history,
    author="Aetf",
    author_email='aetf@unlimitedcodeworks.xyz',
    url='https://github.com/Aetf/plocate',
    packages=[
        'plocate',
    ],
    package_dir={'plocate':
                 'plocate'},
    entry_points={
        'console_scripts': [
            'plocate=plocate.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='plocate',
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
