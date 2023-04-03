#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from setuptools import find_packages
from setuptools import setup

def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()

setup(
    name='mtnmomoapi',
    version='0.0.1',
    license='MIT license',
    description='An easy to use Python wrapper for the MTN MoMo API.',
    long_description='%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.md'))
    ),
    long_description_content_type='text/markdown',
    author='sikaili99',
    author_email='sikaili99@gmail.com',
    url='https://github.com/sikaili99/mtnmomoapi',
    packages=find_packages('mtnmomoapi'),
    package_dir={'': 'mtnmomoapi'},
    py_modules=[splitext(basename(path))[0] for path in glob('mtnmomoapi/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
        'Topic :: Utilities',
    ],
    keywords=[
        'MoMo API', 'MoMo API Python Wrapper', 'MoMo API Python','MTN Zambia MoMO API Python', 'MTN Mobile Money API Python'
    ],
    install_requires=[
        'requests == 2.21.0'
    ]
)