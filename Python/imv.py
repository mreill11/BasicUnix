#!/usr/bin/env python2.7

import getopt
import sys
import os
import time
import string
import tempfile
from os import rename, unlink, path

arg = sys.argv[1:]

fp = tempfile.NamedTemporaryFile(delete=False)

for FILE in arg:
    fp.write(FILE)
    fp.write('\n')
fp.close()


try:
    os.system('${EDITOR:-nano} ' + fp.name)
except OSError:
    sys.exit(1)

temp = open(fp.name)

for a, b in zip(arg,temp):
    try:
        os.rename(a,b.rstrip())
    except OSError as e:
        print e
sys.exit(1)

os.unlink(fp.name)