#!/usr/bin/env python2.7
import os
import sys
import getopt
import yaml
import fnmatch
import time
import re
import shlex

# Global Variables

RULES = 'rorschach.yml'
SECONDS = 2
DIRECTORIES = '.'
VERBOSE = False
PATTERN = ''
ACTION = ''
myDict = {} # initializes a dictionary to be used for the different paths
action = [] # initializes a list that will be used for ACTION

# Functions

def usage(status=0):
    print '''Usage: rorschach.py [-r RULES -t SECONDS] DIRECTORIES...
        
        Options:
        
        -r RULES    Path to rules file (default is .rorschach.yml)
        -t SECONDS  Time between scans (default is 2 seconds)
        -v          Display verbose debugging output
        -h          Show this help message'''.format(os.path.basename(sys.argv[0]))
            sys.exit(status)

def error(message, *args):
    print >>sys.stderr, message.format(*args)
        sys.exit(1)

# checks each file in specified directory to see if it matches any of the rules
def check_directory(d):
    for root, dirs, files in os.walk(d):
        for name in dirs+files:
            if fnmatch.fnmatch(name, PATTERN): # pattern match
                if name not in myDict:	# file in dictionary
                    path = os.path.join(root,name)
                        addfiles(name,path)
                            act = ACTION.format(name=name, path=path) # sets name to name
                                action = shlex.split(act)
                                    execute_action(action)
                                elif name in myDict:
                                    path = os.path.join(root,name)
                                        if myDict[name] != os.path.getmtime(path):
                                            addfiles(name,path)
                                                act = ACTION.format(name=name, path=path) # sets name to name
                                                action = shlex.split(act)
                                                execute_action(action)

# this function executes the action
def execute_action(action):
    try:
        verbose('Forking...')
        pid = os.fork()
        if pid == 0: # Child
            try:
                verbose('Execing...')
                os.execvp(action[0],action)
            except OSError as e:
                error('Unable to exec {}', e)
        else:
            try:
                verbose('Waiting...')
                pid,status = os.wait()
            except OSError as e:
                error('Unable to wait {}', e)
    except OSError as e:
        error('Unable to fork {}', e)


# this function simply prints out what the program is running
def verbose(message):
    if VERBOSE:
        print >>sys.stderr, message

def addfiles(name, path):
    myDict[name] = os.path.getmtime(path)


# Parsing through the command line arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "hvt:r:")
except getopt.GetoptError as e:
    print e
        usage(1)

DIRECTORIES = args # sets the directories to the args category
if DIRECTORIES == []: # if the list is empty, set the directory
    DIRECTORIES = '.'

for opt, arg in opts:
    if opt == '-t':
        SECONDS	= int(arg)
        elif opt == '-r':
            RULES = str(arg)
        elif opt == '-v':
            VERBOSE = True
        else:
            usage(1)

# Parsing the yml file
with open(RULES, 'r') as f:
    doc = yaml.load(f)

PATTERN = doc["pattern"]
ACTION = doc["action"]

# Main Execution
try:
    while True:
        for d in DIRECTORIES:
            check_directory(d)
                time.sleep(SECONDS)
                    os.system('clear')
except KeyboardInterrupt:
    sys.exit(1)