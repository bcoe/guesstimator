#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name="sampy",
      version="0.0.1",
      description="Estimates the performance of a distributed system based on a sample set of data.",
      author="Benjamin Coe",
      author_email="ben@attachments.me",
      entry_points = {},
      url="https://github.com/bcoe/sampy",
      packages = find_packages(),
      install_requires = ['redis'],
      tests_require=['nose']
)
