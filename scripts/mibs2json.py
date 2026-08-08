#!/usr/bin/env python3

"""Parse MIB files and write compressed JSON"""


BASEDIR = '../mibs'
# Hardcoded as it is expected to execute this script from
# the directory is is located in.

OUTFILE = 'mibs.json.bz2'

from pysmi.reader import FileReader, HttpReader
from pysmi.searcher import StubSearcher
from pysmi.writer import CallbackWriter, FileWriter
from pysmi.parser import SmiStarParser
from pysmi.codegen import JsonCodeGen
from pysmi.compiler import MibCompiler
from pysmi import debug

import json
import os
import sys
import collections
import bz2

DATA = collections.defaultdict(dict)
"""Holds the entire data structure."""

MODULE = None
"""Don't know how to pass that info between `writer()` and `worker()`."""

MIBDIRS = []

def writer(mib_name, parsed, context):
    global DATA
    global MODULE

    # See parsed.json for an example of `parsed`.
    d = json.loads(parsed)

    MODULE = d['meta']['module']
    del(d['meta'])

    DATA['imports'][MODULE] = [key for key in d.get('imports', {}).keys() if key != 'class']
    del(d['imports'])

    for key,value in d.items():
        DATA['objects'][f'{MODULE}::{key}'] = value
        DATA['objects'][f'{MODULE}::{key}']['MODULE'] = MODULE
        DATA['oid'][value['oid']] = f'{MODULE}::{key}'


def worker(filepath):
    global MIBDIRS
    global MODULE
    global DATA

    print(filepath, file=sys.stderr)

    try:

        mibCompiler = MibCompiler(
            SmiStarParser(), JsonCodeGen(), CallbackWriter(writer)
        )

        # search for source MIBs here
        mibCompiler.addSources(*[FileReader(x) for x in MIBDIRS])

        # Run recursive MIB compilation
        result = mibCompiler.compile(filepath)

    except KeyError as e:
        raise

    DATA['filepaths'][MODULE] = filepath


def main():
    global DATA
    global MIBDIRS

    # Find all folders under BASEDIR.
    # Find all MIB files.
    for dirpath, dirnames, filenames in os.walk(BASEDIR):
        MIBDIRS.append(dirpath)

    for dirpath, dirnames, filenames in os.walk(BASEDIR):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            worker(filepath)


    with bz2.open(OUTFILE, mode='wt', compresslevel=9) as fp:
        json.dump(DATA, fp, indent=2)

if __name__ == '__main__':
    main()
