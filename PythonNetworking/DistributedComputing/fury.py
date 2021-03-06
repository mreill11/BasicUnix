#!/usr/bin/env python2.7
#David Durkin, Chris Beaufils, Matt Reilly
#fury.py
 
import sys
import work_queue
import os
import hashlib
import itertools
import string
import json
 
# Initializing Constants
ALPHABET = string.ascii_lowercase + string.digits
HASHES = "hashes.txt"
SOURCES = ('hulk.py', HASHES)
PORT = 9548
JOURNAL = {}
 
#Main
if __name__ == '__main__':
   
    #creates a work queue to monitor workers
    queue = work_queue.WorkQueue(PORT, name='hulk-ddurkin2', catalog=True)
    queue.specify_log('fury.log')
   
    for length in range(1,6): #checks passwords of length 6
        command = './hulk.py -l {}'.format(length) #aggregates all words
        #ensures that they are not already in journal
	if command in JOURNAL:
    		print >>sys.stderr, 'Already did', command 
	else:
            task = work_queue.Task(command)
           #adds in source files
            for source in SOURCES:
                task.specify_file(source, source, work_queue.WORK_QUEUE_INPUT)
            queue.submit(task)	       
   
    #goes through guesses of length 6 + a PREFIX of length 1
    for firstprefix in itertools.product(ALPHABET, repeat = 1):
        command = './hulk.py -l 6 -p {}'.format(''.join(firstprefix))
	if command in JOURNAL:
    		print >>sys.stderr, 'Already did', command 
	else:
            task = work_queue.Task(command)

            for source in SOURCES:
                task.specify_file(source, source, work_queue.WORK_QUEUE_INPUT)
            queue.submit(task)
 
    #goes through guesses of length 6 + a PREFIX of length 2
    for secondprefix in itertools.product(ALPHABET, repeat = 2):
        command = './hulk.py -l 6 -p {}'.format(''.join(secondprefix))
	if command in JOURNAL:
    		print >>sys.stderr, 'Already did', command 
	else:
            task = work_queue.Task(command)

            for source in SOURCES:
                task.specify_file(source, source, work_queue.WORK_QUEUE_INPUT)
            queue.submit(task)
 
    while not queue.empty():
        #Wait for a task to complete, is valid, and returned successfullt
        task = queue.wait()

        if task and task.return_status == 0:
            JOURNAL[task.command] = task.output.split()
            with open('journal.json.new', 'w') as stream:
                json.dump(JOURNAL, stream)
            os.rename('journal.json.new', 'journal.json')
