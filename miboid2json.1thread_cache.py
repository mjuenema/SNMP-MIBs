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

import re2 as re

from pysmi.reader import FileReader, HttpReader
from pysmi.searcher import StubSearcher
from pysmi.writer import CallbackWriter, FileWriter
from pysmi.parser import SmiStarParser
from pysmi.codegen import JsonCodeGen
from pysmi.compiler import MibCompiler
from pysmi import debug

import json
import glob
import progressbar

#debug.setLogger(debug.Debug('reader', 'compiler'))

inputMibs = glob.glob('*')


srcDirectories = ['.']

httpSources = [
    ('mibs.snmplabs.com', 80, '/asn1/@mib@')
]


DATA = {}

def writer(mib_name, json_doc, context):

    data = json.loads(json_doc)

    for k,v in data.items():
        try:
            oid = v['oid'].lower()
            name = v['name'].lower()

            DATA[name] = oid
            DATA[oid] = name
        except KeyError:
            pass

for inputMib in progressbar.progressbar(inputMibs):

    try:
        mibCompiler = MibCompiler(
            SmiStarParser(tempdir='.cache'), JsonCodeGen(), CallbackWriter(writer)
        )

        # search for source MIBs here
        mibCompiler.addSources(*[FileReader(x) for x in srcDirectories])

        ## search for source MIBs at Web sites
        #mibCompiler.addSources(*[HttpReader(*x) for x in httpSources])

        # never recompile MIBs with MACROs
        #mibCompiler.addSearchers(StubSearcher(*JsonCodeGen.baseMibs))

        # run recursive MIB compilation
        results = mibCompiler.compile(inputMib)
    except KeyError as e:
        print(inputMib, e)


with open('miboid.json', 'wb') as fp:
    json.dump(DATA, fp, indent=2, sort_keys=True)
