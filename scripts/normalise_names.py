#!/usr/bin/env python3


BASEDIR = '../mibs'
# Hardcoded as it is expected to execute this script from
# the directory is is located in.

from pysmi.reader import FileReader, HttpReader
from pysmi.searcher import StubSearcher
from pysmi.writer import CallbackWriter, FileWriter
from pysmi.parser import SmiStarParser
from pysmi.codegen import JsonCodeGen
from pysmi.compiler import MibCompiler
from pysmi import debug

import pathlib
import os

MODULE = None
"""Don't know how to pass that info between `writer()` and `worker()`."""

MIBDIRS = []

def writer(mib_name, parsed, context):
    global MODULE

    # See parsed.json for an example of `parsed`.
    d = json.loads(parsed)

    # Extract the module name and put it into the global variable.
    MODULE = d['meta']['module']

def worker(filepath):
    global MIBDIRS
    global MODULE
    print(filepath)

    mibCompiler = MibCompiler(
        SmiStarParser(), JsonCodeGen(), CallbackWriter(writer)
    )

    # search for source MIBs here
    mibCompiler.addSources(*[FileReader(x) for x in MIBDIRS])

    # Run recursive MIB compilation
    result = mibCompiler.compile(filepath)

    # At this stage the global variable module will contain
    # the proper name of the MIB file. 

    oldpath = pathlib.Path(filepath)
    newpath = oldpath.parent / MODULE

    print(f"mv {oldpath} {newpath}")


def main():
    global MIBDIRS

    # Find all folders under BASEDIR.
    # Find all MIB files.
    for dirpath, dirnames, filenames in os.walk(BASEDIR):
        MIBDIRS.append(dirpath)

    for dirpath, dirnames, filenames in os.walk(BASEDIR):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            worker(filepath)

if __name__ == '__main__':
    main()
