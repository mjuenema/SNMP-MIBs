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
from multiprocessing import Pool, TimeoutError

import json
import glob


import progressbar

NUM_WORKERS = 50     # TODO: = number of CPU cores

#debug.setLogger(debug.Debug('reader', 'compiler'))

data = {}
"""Holds the entire data structure."""


def writer(mib_name, json_doc, context):
    global data

    d = json.loads(json_doc)

    local_data = {}

    for k,v in d.items():
        try:
            oid = v['oid'].lower()
            name = v['name'].lower()

            local_data[name] = oid
            local_data[oid] = name
        except KeyError:
            # Raised if v[] does not have a 'name' or 'oid' key
            # which is true for all "non OID" entries in a MIB so
            # it's ok.
            pass

    return local_data


def worker(input_mib):

    try:

        srcDirectories = ['.']

        #httpSources = [
        #    ('mibs.snmplabs.com', 80, '/asn1/@mib@')
        #]

        mibCompiler = MibCompiler(
            SmiStarParser(), JsonCodeGen(), CallbackWriter(writer)
        )

        # search for source MIBs here
        mibCompiler.addSources(*[FileReader(x) for x in srcDirectories])

        # search for source MIBs at Web sites
        #mibCompiler.addSources(*[HttpReader(*x) for x in httpSources])

        # never recompile MIBs with MACROs
        #mibCompiler.addSearchers(StubSearcher(*JsonCodeGen.baseMibs))

        # Run recursive MIB compilation
        results = mibCompiler.compile(input_mib)
        return results

    except KeyError as e:
        print(inputMib, e)


def main():
    global data

    input_mibs = glob.glob('*')

    with Pool(processes=4) as pool:
        print(pool.map(worker, input_mibs[:10]))


#    q = queue.Queue(maxsize=NUM_WORKERS+10)
#
#    # Start worker threads
#    #
#    threads = []
#
#    for i in range(0, NUM_WORKERS):
#        thread = threading.Thread(target=worker, args=(q,))
#        threads.append(thread)
#        thread.start()
#
#
#    for input_mib in progressbar.progressbar(input_mibs):
#        q.put(input_mib, block=True, timeout=None)
#
#
#    # Wait until all items in the queue have been processed.
#    #
#    q.join()
#
#
#    # Wait for all threads to complete.
#    #
#    for thread in threads():
#        threda.join()
#
#
#    # Write data to JSON file.
#    #
#    with open('miboid.json', 'wb') as fp:
#        json.dump(data, fp, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
