#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name="sampy",
      version="0.0.1",
      description="Perodically sample arbitrary data. Backed by Redis. Ganglia plugin included.",
      author="Benjamin Coe",
      author_email="ben@attachments.me",
      entry_points = {},
      url="https://github.com/attachmentsme/sampy",
      packages = find_packages(),
      install_requires = ['redis'],
      tests_require=['nose']
)
