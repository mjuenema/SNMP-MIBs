#!/usr/bin/env python3

"""Read all MIBS and create a dependency graph of imports
   as a NetworkX DiGraph. Save the DiGraph in Python pickle
   format.

   The 'parser' are just two regular expressions because I
   neither have the time nor nerves to implement an MIB
   parser.

"""

import networkx
import re
import os
import pickle

graph = networkx.DiGraph()

RE_NAME = re.compile(r'(\S+)\s+DEFINITIONS\s*::=\s* BEGIN')
RE_FROM = re.compile(r'FROM\s+(\S+)')

for dirpath,dirnames,filenames in os.walk('../mibs'):
    for filename in filenames:
        path = os.path.join(dirpath, filename)

        with open(path, 'r', encoding='utf-8', errors='replace') as fp:
            mibname = None

            for line in fp:

                m = RE_NAME.search(line)
                if m:
                    mibname = m.groups()[0].rstrip(';')

                m = RE_FROM.search(line)
                if m:
                    if not mibname:
                        mibname = os.path.basename(path).replace('.mib', '')
                    imported = m.groups()[0].rstrip(';')

                    graph.add_edge(mibname, imported)

with open('imports.pickle', 'wb') as fp:
    pickle.dump(graph, fp, pickle.HIGHEST_PROTOCOL)



#networkx.write_gml(graph, 'dependencies.gml')
#
#dependencies = networkx.descendants(graph, 'CISCO-PORT-SECURITY-MIB')
#print(dependencies)









        
