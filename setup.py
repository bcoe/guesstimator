#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name="guesstimator",
      version="0.0.2",
      description="Estimates the performance of a distributed system based on a sample set of data.",
      author="Benjamin Coe",
      author_email="ben@attachments.me",
      entry_points = {},
      url="https://github.com/bcoe/guesstimator",
      packages = find_packages(),
      install_requires = ['redis'],
      tests_require=['nose']
)
