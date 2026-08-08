#!/usr/bin/env python3


BASEDIR = '../mibs'
# Hardcoded as it is expected to execute this script from
# the directory is is located in.

import pathlib
import os
import re

REGEX = re.compile(r'(\S+)\s*DEFINITIONS\s*::=\s*BEGIN')

def main():
    for dirpath, dirnames, filenames in os.walk(BASEDIR):
        for filename in filenames:
            filepath = pathlib.Path(os.path.join(dirpath, filename))

            with open(filepath, 'rt', encoding='utf-8', errors='ignore') as fp:
                for line in fp:
                    m = REGEX.search(line)
                    if m:
                        module = m.groups()[0]
                        newpath = filepath.parent / module
                        if newpath != filepath:
                            try:
                                print(f"mv {filepath} {newpath}")
                                filepath.rename(newpath)
                            except FileNotFoundError:
                                pass
                        break


if __name__ == '__main__':
    main()
