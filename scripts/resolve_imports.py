#!/usr/bin/env python3

"""Read snmptrap.json and resolve all OIDs to MIB modules so
   I know what modules are actually needed
"""

import bz2
import json
import sys

with bz2.open('mibs.json.bz2', 'rt') as fp:
    MIBDATA = json.load(fp)


def resolve(mibname):
    global IMPORTS

    if mibname not in IMPORTS:
        IMPORTS.add(mibname)

        for mibname in MIBDATA['imports'][mibname]:
            resolve(mibname)


IMPORTS = set()

for mibname in sys.argv[1:]:
#mibname = sys.argv[1]
    resolve(mibname)

for mibname in IMPORTS:
    print(mibname.upper())



#mibs = set(sys.argv[1:])




#oldlen = len(mibs)
#newlen = 0
#
#while oldlen != newlen:
#    oldlen = len(mibs)
#    for mib in mibs:
#        try:
#            mibs.union(mibdata['imports'][mib])
#        except KeyError:
#            print(f"*{mib}")
#    newlen = len(mibs)

#for mib in mibs:
#    try:
#        print(mibdata['imports'][mib])
#    except KeyError:
#        print(f"*{mib}")




