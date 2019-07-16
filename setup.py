# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

if __name__ == "__main__":
    here = os.path.abspath(os.path.dirname(__file__))
    about = {}
    with open(os.path.join(here, 'excalibur', '__version__.py'), 'r') as f:
        exec(f.read(), about)
    __version__ = about['__version__']

    setup(use_scm_version=True)
