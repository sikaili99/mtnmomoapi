#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='mtnmomoapi',
    version='0.0.1',
    license='MIT license',
    author = "Mathews Musukuma",
    author_email = "sikaili99@gmail.com",
    description = "An easy to use Python wrapper for the MTN MoMo API.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/sikaili99/mtnmomoapi",
    project_urls = {
        "Bug Tracker": "https://github.com/sikaili99/mtnmomoapi/issues",
        "repository" : "https://github.com/sikaili99/mtnmomoapi"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        'MoMo API', 'MoMo API Python Wrapper', 'MoMo API Python','MTN Zambia MoMO API Python', 'MTN Mobile Money API Python'
    ],
    package_dir = {"": "src"},
    packages = find_packages(where="src"),
    python_requires = ">=3.6"
)
