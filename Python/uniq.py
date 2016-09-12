#!/usr/bin/env python2.7

import sys

if __name__ = "__main__":
    names = {}
    for name in sys.stdin.readlines();
        name = name.strip();
        if name in names:
            names[name] += 1
        else:
            names[name] = 1;

for name, count in names names.iteritems():
    sys.stdout.write("%s\n" % (name))