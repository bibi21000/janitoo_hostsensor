#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup file of Janitoo
"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014 Sébastien GALLET aka bibi21000"

from os import name as os_name
from setuptools import setup, find_packages
from platform import system as platform_system
import glob
import os
import sys
from _version import janitoo_version

DEBIAN_PACKAGE = False
filtered_args = []

for arg in sys.argv:
    if arg == "--debian-package":
        DEBIAN_PACKAGE = True
    else:
        filtered_args.append(arg)
sys.argv = filtered_args

def data_files_config(target, source, pattern):
    ret = list()
    ret.append((target, glob.glob(os.path.join(source,pattern))))
    dirs = [x for x in glob.iglob(os.path.join( source, '*')) if os.path.isdir(x) ]
    for d in dirs:
        rd = d.replace(source+os.sep, "", 1)
        ret.extend(data_files_config(os.path.join(target,rd), os.path.join(source,rd), pattern))
    return ret

data_files = data_files_config('docs','src/docs','*.rst')
data_files.extend(data_files_config('docs','src/docs','*.md'))
data_files.extend(data_files_config('docs','src/docs','*.txt'))
data_files.extend(data_files_config('docs','src/docs','*.png'))
data_files.extend(data_files_config('docs','src/docs','*.jpg'))
data_files.extend(data_files_config('docs','src/docs','*.gif'))

#You must define a variable like the one below.
#It will be used to collect entries without installing the package
janitoo_entry_points = {
    "janitoo.threads": [
        "hostsensor = janitoo_hostsensor.hostsensor:make_thread",
    ],
    "janitoo.components": [
        "hostsensor.load = janitoo_hostsensor.hostsensor:make_load",
    ],
}

setup(
    name = 'janitoo_hostsensor',
    description = "A controller for local sensors (lmsensors, cpu, disk, ...)",
    long_description = "A controller for local sensors (lmsensors, cpu, disk, ...)",
    license = """
        This file is part of Janitoo.

        Janitoo is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        Janitoo is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with Janitoo. If not, see <http://www.gnu.org/licenses/>.
    """,
    author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
    author_email='bibi21000@gmail.com',
    url='http://bibi21000.gallet.info/',
    version = janitoo_version,
    keywords = "computer,cpu",
    zip_safe = False,
    package_dir = { '': 'src' },
    packages = find_packages('src', exclude=["scripts", "docs", "config"]),
    include_package_data=True,
    data_files = data_files,
    install_requires=[
                     'janitoo >= %s'%"0.0.6",
                    ],
    dependency_links = [
      'https://github.com/bibi21000/janitoo/archive/master.zip#egg=janitoo-%s'%"0.0.7",
    ],
    entry_points = janitoo_entry_points,
)
