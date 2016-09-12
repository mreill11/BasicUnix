#!/usr/bin/env python2.7

import sys
import getopt

def usage():
	print """usage: wc.py [-d DELIM -f FIELDS] files ...
	
		-d DELIM ise DELIM instead of TAB for field delimiter
		-f FIELDS select only these FIELDS"""
DELIM = '\t'
FIELDS = 0

try:
	opts, args = getopt.getopt(sys.argv[1:], 'hd:f:'
except getopt.GetoptError as e:
	print e

for o, a in opts:
	if o == '-d':
		DELIM = a
	elif o == '-f':
		FIELDS = a
	elif o == '-h':
		usage()
		exit(1)

if len(args) == 0:
	args.append('-')

splitfields = FIELDS.split(',')

# Main

for path in args:
	if path == '-':
		stream = sys.stdin
	else:
		stream = open(path)
	
	file = stream.read()
	splitfile = file.splitlines()
	for line in splitfile:
		splitline = line.split(DELIM)
		for field in splitfields:
			sys.stdout.write(splitline[field])
			sys.stdout.write(' ')
		sys.stdout.write('\n')