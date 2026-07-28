#!/usr/bin/env python

"""
Compile MIBs into JSON
++++++++++++++++++++++

Look up specific ASN.1 MIBs at configured Web and FTP sites,
compile them into JSON documents and print them out to stdout.

Try to support both SMIv1 and SMIv2 flavors of SMI as well as
popular deviations from official syntax found in the wild.
"""#

from __future__ import print_function
from pysmi.reader import FileReader, HttpReader
from pysmi.searcher import StubSearcher
from pysmi.writer import CallbackWriter, FileWriter
from pysmi.parser import SmiStarParser
from pysmi.codegen import JsonCodeGen
from pysmi.compiler import MibCompiler
from pysmi import debug

import json
import glob

#debug.setLogger(debug.Debug('reader', 'compiler'))

inputMibs = glob.glob('*')

srcDirectories = ['.']

#httpSources = [
#    ('mibs.snmplabs.com', 80, '/asn1/@mib@')
#]


DATA = {}


def writer(mib_name, json_doc, context):

    data = json.loads(json_doc)

    for k,v in data.items():
        DATA[v.get('oid')] = v.get('name')
        DATA[v.get('name')] = v.get('oid')

for inputMib in inputMibs:
    print(inputMib)

    try:

        mibCompiler = MibCompiler(
            SmiStarParser(), JsonCodeGen(), CallbackWriter(writer)
        )

        # search for source MIBs here
        mibCompiler.addSources(*[FileReader(x) for x in srcDirectories])

        # search for source MIBs at Web sites
        #mibCompiler.addSources(*[HttpReader(*x) for x in httpSources])

        # never recompile MIBs with MACROs
        #mibCompiler.addSearchers(StubSearcher(*JsonCodeGen.baseMibs))

        # run recursive MIB compilation
        results = mibCompiler.compile(inputMib)

    except Exception as e:
        print(e)

with open('/tmp/mibs.json', 'wb') as fp:
    json.dump(DATA, fp)
