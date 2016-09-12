#!/usr/bin/env python2.7

import sys
import getopt

def usage():
	print """Usage: head.py [-c -l -w] files ...
	
		-c	print the byte/character counts
		-l	print the newline counts
		-w	print the word counts"""

apply = 'none'

try:
	opts, args = getopt.getopt(sys.argv[1:], 'clwh')
except getopt.GetOptError as e:
	print e

for o,a in opts:
	if o == '-c':
		apply = 'character'
	elif o == '-l':
		apply = 'lines'
	elif o == '-w':
		apply = 'words'
	elif o == '-h':
		usage()
		exit(1)

if apply == 'none':
	print "error - no flag was passed."
	usage()

if len(args) == 0:
	args.append('-')

# Main execution

for path in args:
	if path == '-':
		stream = sys.stdin
	else:
		stream = open(path)
	file = stream.read()
	if apply == 'character':
		print len(file)
	if apply == 'lines':
		splitfile = file.splitlines()
		print len(splitfile)
	if apply == 'words':
		splitfile = file.split()
		print len(splitfile)


