'''
Copyright (C) 2017 Scaleway. All rights reserved.
Use of this source code is governed by a MIT-style
license that can be found in the LICENSE file.
'''

import os
from setuptools import setup, find_packages

def read(shortname):
    filename = os.path.join(os.path.dirname(__file__), shortname)
    with open(filename, encoding='utf-8') as f:
        contents = f.read()
    return contents

setup(
    name="testinfra_tim",
    version="0.0.1",
    author="Scaleway",
    author_email="opensource@scaleway.com",
    scripts=['yamltest'],
    description="A pytest plugin reading tests from a yaml file.",
    license="MIT",
    keywords="pytest testinfra yaml",
    url="https://github.com/scaleway/tim",
    packages=find_packages(),
    python_requires='>= 3.3',
    install_requires=['testinfra', 'pyyaml'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
    ],
)
