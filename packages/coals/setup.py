#!/usr/bin/python3
#
# Copyright 2018 British Broadcasting Corporation
#
# Author: Michael Sparks <michael.sparks@bbc.co.uk>
#
# All Rights Reserved
#

from distutils.core import setup
from distutils.version import LooseVersion
import os

def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base="" ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if os.path.isdir(dir):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            if is_package( dir ):
                packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages


packages = find_packages(".")
package_names = packages.keys()

setup(name = "coals",
      version = "0.1.2",
      description = "An Adaptive Learning System Core",
      author='Michael Sparks',
      author_email="michael.sparks@bbc.co.uk",
      license='All Rights Reserved',

      scripts = [
                  "bin/coals"
                ],

      packages = package_names,
      package_dir = packages,
      package_data={},
      long_description = """
coals - An Adaptive Learning System Core
----------------------------------------

"""
      )
