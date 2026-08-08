#!/usr/bin/env python3

"""Create a mapping of IANA Enterprise numbers to folders
   inside the mibs/ folder. This can be used later to automatically 
   sort MIBs into folders.

"""


import pathlib
import os
import re
import sys
import json

REGEX = re.compile(r'::=\s*{\s*enterprises\s+(\d+)')

basedir = '../mibs'
# Hardcoded as it is expected to execute this script from
# the directory is is located in.

data = {}

for dirpath, dirnames, filenames in os.walk(basedir):
    for filename in filenames:
        filepath = pathlib.Path(os.path.join(dirpath, filename))

        with open(filepath, 'rt', encoding='utf-8', errors='ignore') as fp:
            for line in fp:
                m = REGEX.search(line)
                if m:
                    number = int(m.groups()[0])
                    data[number] = filepath.parent

print(json.dumps(data), indent=2)


