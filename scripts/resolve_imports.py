#!/usr/bin/env python3

"""Read snmptrap.json and resolve all OIDs to MIB modules so
   I know what modules are actually needed
"""

import bz2
import json
import sys

with bz2.open('mibs.json.bz2', 'rt') as fp:
    mibdata = json.load(fp)

mibs = set(sys.argv[1:])
oldlen = len(mibs)
newlen = 0

while oldlen != newlen:
    oldlen = len(mibs)
    for mib in mibs:
        try:
            mibs.union(mibdata['imports'][mib])
        except KeyError:
            print(f"*{mib}")
    newlen = len(mibs)

for mib in mibs:
    try:
        print(mibdata['filepaths'][mib])
    except KeyError:
        print(f"*{mib}")




