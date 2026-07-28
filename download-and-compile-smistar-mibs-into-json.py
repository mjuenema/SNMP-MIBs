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
import re

#debug.setLogger(debug.Debug('reader', 'compiler'))

#inputMibs = ['IF-MIB', 'IP-MIB']
#inputMibs = ['CISCO-PRODUCTS-MIB']

inputMibs = []

for path in glob.glob('*'):
    with open(path) as fp:
        content = fp.read()
        if len(re.findall('products', content, flags=re.IGNORECASE)) > 2:
            print('+', path)
            inputMibs.append(path)
        else:
            print('-', path)


srcDirectories = ['/usr/share/snmp/mibs', '.']
httpSources = [
    ('mibs.snmplabs.com', 80, '/asn1/@mib@')
]


DATA = {}


def writer(mib_name, json_doc, context):

    data = json.loads(json_doc)

    for k,v in data.items():
        if v.get('class') == 'objectidentity' and v.get('oid').startswith('1.3.6.1.4.1'):
            DATA[v.get('oid')] = v.get('name')

    #with open('/tmp/{}.json'.format(mib_name) , 'wb') as fp:
    #    fp.write(json_doc)


for inputMib in inputMibs:
    print('*',inputMib)

    try:

        mibCompiler = MibCompiler(
            SmiStarParser(), JsonCodeGen(), CallbackWriter(writer)
        )

        # search for source MIBs here
        mibCompiler.addSources(*[FileReader(x) for x in srcDirectories])

        # search for source MIBs at Web sites
        mibCompiler.addSources(*[HttpReader(*x) for x in httpSources])

        # never recompile MIBs with MACROs
        mibCompiler.addSearchers(StubSearcher(*JsonCodeGen.baseMibs))

        # run recursive MIB compilation
        results = mibCompiler.compile(inputMib)
        #print(results)

    except Exception as e:
        print(e)

#print(json.dumps(DATA))

with open('/tmp/mibs.json', 'wb') as fp:
    json.dump(DATA, fp)
