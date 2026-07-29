#!/usr/bin/env python3

"""Normalise the filenames to match the name of a MIB.

     XPPC-MIB DEFINITIONS ::= BEGIN 
     ^^^^^^^^

   This is quick-and-dirty implementation and must be
   executed from with the mibs/ folder.

"""

import glob
import os
import re
import sys

# Quick test that we are in the mibs/ folder
os.stat('XPPC-MIB')

for name1 in glob.glob('*'):
#    print(name1, file=sys.stderr)
    name2 = None
    with open(name1, 'rt') as fp:
        try:
            for line in fp:
                m = re.match(r'^(\S+)\s+DEFINITIONS\s+::=\s+BEGIN', line)
                if m:
                    name2 = f"{m.groups()[0].upper()}.mib"
        except UnicodeDecodeError:
            # Cannot deal with that at the moment
            pass

    if name2 is None:
        # Is this a MIB file?
        pass
    elif name1 != name2:
        print(f"git mv {name1} {name2} || git rm {name1}")
        # git rm in case of duplicates




