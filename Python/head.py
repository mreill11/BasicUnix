#!/usr/bin/env python2.7

import getopt
import sys

def read_file(filename):
	arr = []
	f = open(filename, mode='r')
	for lines in f:
		arr.append(lines)
	return arr

def usage(status=0):
	print '''usage: head.py [-n NUM] files ...

	-n NUM print the first NUM lines instead of the first 10'''.format(os.path.basename(sys.argv[0]))
	sys.exit(status)

x = 10

try:
	opts, args = getopt.getopt(sys.argv[1:], "hn")
except getopt.GetoptError as e:
	print e
	usage(1)

for o, a in opts:
	if 0 == '-n':
		x = int(args[0])
	else:
		usage(1)

		