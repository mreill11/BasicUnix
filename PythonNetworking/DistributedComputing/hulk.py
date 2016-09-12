#!/usr/bin/env python2.7

# Hulk.py
# Smash MD5 Hashes, Hulk style
# David Durkin, Chris Beaufils, David Durkin

import sys
import os
import getopt
import hashlib
import string
import random
import itertools

# Defining Constants
ALPHABET = string.ascii_lowercase + string.digits
LENGTH = 8
HASHES = 'hashes.txt'
PREFIX = ''

# Functions
def usage(status=0):
	print >>sys.stderr, '''Usage: hulk.py [-a ALPHABET -l LENGTH -s HASHES -p PREFIX]
	
Options:
	-a ALPHABET		Alphabet used for passwords
	-l LENGTH		Length for passwords
	-s HASHES		Path to file containing hashes
	-p PREFIX 		Prefix to use for each candidate password'''
	sys.exit(status)

# Compute MD5 hash of string
def md5sum(s):
	return hashlib.md5(s).hexdigest()
	
# Main Execution
if __name__ == '__main__':
	# Parsing command line arguments
	try:
		options, arguments = getopt.getopt(sys.argv[1:], "a:l:s:p:")
	except getopt.GetoptError as e:
		usage(1)
	

	for opt, arg in options:
		if opt == '-a':
			ALPHABET = str(arg)
		elif opt == '-l':
			LENGTH = int(arg)
		elif opt == '-s':
			HASHES = str(arg)
		elif opt == '-p':
			PREFIX = str(arg)
		else:
			usage(1)
			
	# Create a massive list of every possible password, given length
	permutations = itertools.product(ALPHABET , repeat=LENGTH)

	# Use a set
	# Storing value with key is a waste
	hashes = set([line.strip() for line in open(HASHES)])
	cracked = set()
	
	for permutation in permutations:
		possiblePass = ''.join(permutation) # concatenate str and tuple
		possiblePass = PREFIX + possiblePass
		
		guess = md5sum(possiblePass)
		if guess in hashes:
			cracked.add(possiblePass)
	
	totalLen = LENGTH + len(PREFIX)
	for possiblePass in sorted(cracked):
		if len(possiblePass) == totalLen:
			print possiblePass

			