#!/usr/bin/env python3

"""Add MIBs that are missing"""


import pathlib
import os
import re
import sys

basedir = '../mibs'
# Hardcoded as it is expected to execute this script from
# the directory is is located in.

otherdir = sys.argv[1]
data = set()

for dirpath, dirnames, filenames in os.walk(basedir):
    for filename in filenames:
        filepath = pathlib.Path(os.path.join(dirpath, filename))
        data.add(filepath.name)

for dirpath, dirnames, filenames in os.walk(otherdir):
    for filename in filenames:
        filepath = pathlib.Path(os.path.join(dirpath, filename))

        if filepath.name.upper() not in data:
            print(f"cp {filepath} {basedir}/UNSORTED")

