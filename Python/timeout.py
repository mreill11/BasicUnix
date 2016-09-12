#!/usr/bin/env python2.7

import getopt
import os
import sys
import time
import signal

# Global Variables
SECONDS = 10
VERBOSE = False
try:
    COMMAND = ' '.join(sys.argv[1:])
except OSError:
    usage(1)

# Functions

def error(message, exit_code=1):
    print >>sys.stderr, message
        sys.exit(exit_code)

def usage(exit_code=0):
    error('''Usage: timeout.py [-t SECONDS] command...
        
        Options:
        
        -t SECONDS  Timeout duration before killing command (default is 10 seconds)
        -v          Display verbose debugging output'''.format(os.path.basename(sys.argv[0])))


def debug(message, *args):
    if VERBOSE:
        print >> sys.stderr,message.format(*args)

def alarm_handler(signum, frame):
    global ChildPid, ChildStatus
        debug('Alarm Triggered after {} seconds!',int(SECONDS))
        debug('Killing PID {}...'.format(pid))
        os.kill(pid, signal.SIGTERM)



# Parse Command Line Args

try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:v")
except getopt.GetoptError as e:
    print e
        usage(1)

for opt, arg in opts:
    if opt == '-t':
        SECONDS = float(arg)
        #COMMAND = ' '.join(sys.argv[3:])
        elif opt == '-v':
            VERBOSE = True
        else:
            usage(1)

COMMAND = ' '.join(args)
if len(args) == 0:
    args.append('-')

# Main Execution

debug('Executing "{}" for at most {} seconds...', COMMAND, int(SECONDS))

try:
    debug('Forking...', COMMAND, SECONDS)
        pid = os.fork()

except OSError as e:# Error
    error('Unable to fork: {}', e)

if pid == 0:    # Child
    try:
        debug("Execing ...", COMMAND, SECONDS)
            os.execvp(args[0], args)
    
        except OSError as e:
            error('Unable to exec: {}', e)
else:           # Parent
    debug('Enabling Alarm...')
        signal.signal(signal.SIGALRM, alarm_handler)
        debug('Waiting...', COMMAND, SECONDS)
        signal.alarm(int(SECONDS))
        try:
            pid,status = os.wait()
        except OSError:
            pid,status = os.wait()
        debug('Disabling Alarm...')
        debug('Process {} terminated with exit status {}'.format(pid,status))
                sys.exit(status)
