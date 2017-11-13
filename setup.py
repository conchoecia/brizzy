#!/usr/bin/env python3

# Brizzy - easy Ocean Optics spectra capture.
# Copyright (c) 2016-2017 Darrin T. Schultz. All rights reserved.
#
# This file is part of brizzy.
#
# brizzy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# brizzy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with brizzy.  If not, see <http://www.gnu.org/licenses/>.

# Tutorials on how to setup python package here:
#   - http://python-packaging.readthedocs.io/en/latest/testing.html
#   - https://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/

import os
from setuptools import setup, find_packages

version_py = os.path.join(os.path.dirname(__file__), 'brizzy', 'version.py')
version = open(version_py).read().strip().split('=')[-1].replace('"','').strip()
print("Setup.py thinks the current brizzy version is {}".format(version))


setup(name='brizzy',
      requires=['python (>3.0)'],
      version=version,
      description='Tools for plotting Oxford Nanopore and other long-read data.',
      # sorry for the ugly indent formatting. I had to do this for PyPi's sake.
      long_description="""
          'brizzy' is a package for easily taking spectra from ocean optics
      spectrometers. No more hitting the pause button every time you want a
      spectrum!

      You can visit the gitub page for more detailed information here:
      https://github.com/conchoecia/brizzy
      """,

      url='https://github.com/conchoecia/brizzy',
      author='Darrin Schultz',
      author_email='dts@ucsc.edu',
      classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Operating System :: POSIX :: Linux',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Intended Audience :: Science/Research'
          ],
      license='GPLv3',
      provides=['brizzy'],
      packages=find_packages(),
      install_requires=[
          "matplotlib >= 2.0.2",
          "pandas >= 0.20.1",
          "numpy >= 1.12.1",
          "scipy >= 0.19.0",
          "progressbar2 >= 3.18.1"
      ],
      entry_points={
            'console_scripts': ['brizzy=brizzy.brizzy_main:main'],
        },
      zip_safe=False,
      include_package_data=True)
