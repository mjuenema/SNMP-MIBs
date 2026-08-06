#!/usr/bin/env python3

"""Extract OIDs and identifier from SNMP MIBs and
   create a JSON file with mappings between them.

   Check miboid.json for the generated output.

"""

BASEDIR = '../mibs'
# Hardcoded as it is expected to execute this script from
# the directory is is located in.

OUTFILE = 'miboid.json'

from pysmi.reader import FileReader, HttpReader
from pysmi.searcher import StubSearcher
from pysmi.writer import CallbackWriter, FileWriter
from pysmi.parser import SmiStarParser
from pysmi.codegen import JsonCodeGen
from pysmi.compiler import MibCompiler
from pysmi import debug
from multiprocessing import Pool, TimeoutError

import json
import os
import sys
import progress.bar
import threading
import multiprocessing.pool


DATA = {}
"""Holds the entire data structure."""

LOCK = threading.Lock()

MIBDIRS = []

PROGRESS = None


def writer(mib_name, json_doc, context):
    global DATA
    global LOCK

    d = json.loads(json_doc)

    module = d['meta']['module']

    local_data = {}

    for k,v in d.items():
        try:
            oid = v['oid'].lower()
            name = f"{module}::{v['name'].lower()}"

            local_data[name] = oid
            local_data[oid] = name
        except KeyError:
            # Raised if v[] does not have a 'name' or 'oid' key
            # which is true for all "non OID" entries in a MIB so
            # it's ok.
            pass

    with LOCK:
        DATA.update(local_data)

    return local_data


def worker(input_mib):
    global MIBDIRS
    global PROGRESS
    global LOCK

    with LOCK:
        PROGRESS.next()

    try:

        mibCompiler = MibCompiler(
            SmiStarParser(), JsonCodeGen(), CallbackWriter(writer)
        )

        # search for source MIBs here
        mibCompiler.addSources(*[FileReader(x) for x in MIBDIRS])

        # Run recursive MIB compilation
        results = mibCompiler.compile(input_mib)
        return results

    except KeyError as e:
        raise


def main():
    global DATA
    global MIBDIRS
    global PROGRESS

    input_mibs = []

    # Find all folders under BASEDIR.
    # Find all MIB files.
    for dirpath, dirnames, filenames in os.walk(BASEDIR):
        MIBDIRS.append(dirpath)

        for filename in filenames:
            input_mibs.append(os.path.join(dirpath,filename))


    PROGRESS = progress.bar.Bar('Processing', max=len(input_mibs), suffix='%(index)d/%(max)d %(percent)d%%')

    with multiprocessing.pool.ThreadPool(8) as pool:
        pool.map(worker, input_mibs)

    with open(OUTFILE, 'wt') as fp:
        json.dump(DATA, fp)

    PROGRESS.finish()


if __name__ == '__main__':
    main()
