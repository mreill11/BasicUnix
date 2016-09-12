#!/usr/local/bin/python2.7

import getopt
import sys
import os
import re
import fnmatch
import stat

#Global Variables
PROGRAM_NAME = os.path.basename(sys.argvf[0])
READ = False
WRITE = False
EXEC = False
EMPTY = False
filetype = ''
namepat = ''
pathpat = ''
regexpat = ''
modified = ''
mode = 0
user = 0
group = 0
UIDFLAG = 0
GIDFLAG = 0

def error(message, exit_code=1):
    print >> sys.stderr, message
    sys.exit(exit_code)

def usage(exit_code=0):
    error('''Usage: {}
        Options:
        
        -type [f|d]     File is of type f for regular file or d for directory
        
        -executable     File is executable and directories are searchable to user
        -readable       File readable to user
        -writable       File is writable to user
        
        -empty          File or directory is empty
        
        -name  pattern  Base of file name matches shell pattern
        -path  pattern  Path of file matches shell pattern
        -regex pattern  Path of file matches regular expression
        
        -perm  mode     File's permission bits are exactly mode (octal)
        -newer file     File was modified more recently than file
        
        -uid   n        File's numeric user ID is n
        -gid   n        File's numeric group ID is n'''
          .format(PROGRAM_NAME), exit_code)

#Functions
def include(path):
    if filetype != '':
        if filetype == 'f' and not os.path.isfile(path):
            return False
        elif filetype == 'd' and not os.path.isdir(path):
            return False
    if EXEC and not os.access(path, os.X_OK):
        return False
    if READ and not os.access(path, os.R_OK):
        return False
    if WRITE and not os.access(path, os.W_OK):
        return False
    if ISEMPTY:
        if os.path.isfile(path) and os.path.getsize(path) != 0:
            return False
        try:
            if os.path.isdir(path) and len(os.listdir(path)) != 0:
                return False
        except OSError:
            return False
        if os.path.islink(path) and not os.path.exists(os.readlink(path)):
            return False
    if name != '':
        if not fnmatch.fnmatch(os.path.basename(path), name):
            return False
    if path != '':
        if not fnmatch.fnmatch(os.path.basename(path), name):
            return False
    if regex != '':
        if not re.search(regex, path):
            return False
    try:
        info = os.stat(path)
    except OSError:
        info = os.lstat(path)
    if mode != 0:
        if not (stat.S_IMODE(info.st_mode) == mode):
            return False
    if modified != '':
        if (info.st_mtime <= os.stat(modified).st_mtime):
            return False

if UIDFLAG != 0:
    if info.st_uid != user:
        return False
    if GIDFLAG != 0:
        if info.st_gid != group:
            return False
return True

#Parse command line arguments
directory = sys.argv[1]
args = sys.argv[2:]
i = 0
while i < len(args):
    if args[i] == '-type':
        filetype = args[i+1]
        i = i + 1
    elif args[i] == '-executable':
        EXEC = True
    elif args[i] == '-readable':
        READ = True
    elif args[i] == '-writable':
        WRITE == True
    elif args[i] == '-empty':
        EMPTY = True
    elif args[i] == '-name':
        name = args[i+1]
        i = i + 1
    elif args[i] == '-path':
        path = args[i+1]
        i = i + 1
    elif args[i] == '-regex':
        regex = args[i+1]
        i = i + 1
    elif args[i] == '-perm':
        mode = int(args[i+1], 8)
        i = i + 1
    elif args[i] == '-newer':
        modified = args[i+1]
        i = i + 1
    elif args[i] == '-uid':
        UIDFLAG = 1
        user = int(args[i+1])
        i = i + 1
    elif args[i] == '-gid':
        GIDFLAG = 1
        group = int(args[i+1])
        i = i + 1
    i = i + 1

if include(directory):
    print directory
for root, dir, files in os.walk(directory, followlinks=True):
    for name in dires + files:
        check = os.path.join(root, name)
        if include(check):
            print os.path.join(root, name)