#!/usr/local/bin/python2.7

import getopt
import os
import sys


FILESOURCE = 0
FILEDEST = 1
SEEKNUM = 0
SKIPNUM = 0
WRITETOFILE = False
BLOCKSIZE = 512
COUNT = sys.maxint
THEREISCOUNT = False

# Functions
def error(message, exit_code=1):
    print >> sys.stderr,message
        sys.exit(exit_code)

def usage(exit_code=0):
    error('''Usage: {} Options:
        if=FILE		Read from FILE instead of stdin
        of=FILE		Write to FILE instead of stdout
        
        count=N		Copy only N input blocks
        bs=BYTES	Read and write up to BYTES bytes at a time
        
        seek=N		Skip N obs-sized blocks at start of output
        skip=N		Skip N ibs-sized blocks at start of input'''
          .format(PROGRAM_NAME),exit_code)

def open_fd (path,mode):
    try:
        return os.open(path, mode)
        except OSError as e:
            error('Could not open {}: {}'.format(FILESOURCE, e))

def read_fd (fd, n):
    try:
        return os.read(fd, n)
        except OSError as e:
            error('Could not read {} bytes from FD {}: {}'.format(n, fd, e))

def write_fd(fd, data):
    try:
        return os.write(fd, data)
        except OSError as e:
            error('Could not write {} bytes from FD {}: {}'.format(len(data),fd,e))

def lseek_fd(fd, pos, how):
    try:
        return os.lseek(fd, pos, how)
        except OSError as e:
            error('Could not skip {} bytes from FD {}: {}'.format(pos, fd, e))

# Parse Command line arguments
for section in sys.argv[1:]:
    opt = section.split('=')[0]
        arg = section.split('=')[1]
        if opt == 'if':
            FILESOURCE = open_fd(arg, os.O_RDONLY)
        if opt == 'of':
            FILEDEST = open_fd(arg, os.O_WRONLY|os.O_CREAT)
        if opt == 'count':
            THEREISCOUNT = True
                COUNT = int(arg)
        if opt == 'bs':
            BLOCKSIZE = int(arg)
        if opt == 'seek':
            SEEKNUM = int(arg)
        if opt == 'skip':
            SKIPNUM = int(arg)

#Main Execution
n=1
if FILESOURCE !=0:
    if SKIPNUM:
        lseek_fd(FILESOURCE, SKIPNUM * BLOCKSIZE, 0)

if FILEDEST !=1:
    if SEEKNUM:
        lseek_fd(FILEDEST, SEEKNUM * BLOCKSIZE, 0)

data='string'
while n <= COUNT and data != '':
    data= read_fd(FILESOURCE, BLOCKSIZE)
        write_fd(FILEDEST, data)
        n=n+1

os.close(FILESOURCE)
os.close(FILEDEST)