#!/usr/bin/env python2.7

import getopt
import logging
import os
import socket
import sys
import time
import errno

# Constants

ADDRESS  = '127.0.0.1'
PORT     = 80
PROGRAM  = os.path.basename(sys.argv[0])
LOGLEVEL = logging.INFO
PROCESSES = 1
REQUESTS = 1
TIME = False
AVG = False


# Utility Functions

def usage(exit_code=0):
    print >>sys.stderr, '''Usage: thor.py [-r REQUESTS -p PROCESSES -v] URL
        
        Options:
        
        -h           Show this help message
        -v           Set logging to DEBUG level
        
        -r REQUESTS  Number of requests per process (default is 1)
        -p PROCESSES Number of processes (default is 1)
        '''.format(port=PORT, program=PROGRAM)
    sys.exit(exit_code)

# TCPClient Class

class TCPClient(object):
    
    def __init__(self, address=ADDRESS, port=PORT):
        ''' Construct TCPClient object with the specified address and port '''
        self.logger  = logging.getLogger()                              # Grab logging instance
        self.socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Allocate TCP socket
        self.address = address                                          # Store address to listen on
        self.port    = port                                             # Store port to lisen on
    
    def handle(self):
        ''' Handle connection '''
        self.logger.debug('Handle')
        raise NotImplementedError
    
    def run(self):
        ''' Run client by connecting to specified address and port and then
            executing the handle method '''
        try:
            # Connect to server with specified address and port, create file object
            self.socket.connect((self.address, self.port))
            self.stream = self.socket.makefile('w+')
        except socket.error as e:
            self.logger.error('Could not connect to {}:{}: {}'.format(self.address, self.port, e))
            sys.exit(1)
    
        self.logger.debug('Connected to {}:{}...'.format(self.address, self.port))
        
        # Run handle method and then the finish method
        try:
            self.handle()
        except Exception as e:
            self.logger.exception('Exception: {}'.format(e))
        finally:
            self.finish()

    def finish(self):
        ''' Finish connection '''
        self.logger.debug('Finish')
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass    # Ignore socket errors
        finally:
            self.socket.close()

# HTTPClient Class

class HTTPClient(TCPClient):
    
    def __init__(self, url):
        TCPClient.__init__(self, None, None) #Initialize base class
        
        # Parse URL
        self.url = url.split('://')[-1]
        
        if '/' not in self.url:
            self.path = '/'
            self.host = self.url
            self.port = int(PORT)
        else:
            self.path = '/' + self.url.split('/', 1)[-1]
            self.host = self.url.split('/', 1)[0]
            self.port = int(PORT)
            if ':' in self.url:
                partial = self.url.split(':',1)[-1]
                self.host = self.url.split(':', 1)[0]
                if '/' not in partial:
                    self.port = int(partial)
                else:
                    self.port = int(partial.split('/',1)[0])
            
            if '?' in self.path:
                self.path = self.path.split('?', 1)
                self.path = self.path[0]


        self.address = socket.gethostbyname(self.host)
    
        self.logger.debug('URL: {}'.format(self.url))
        self.logger.debug('HOST: {}'.format(self.host))
        self.logger.debug('PORT: {}'.format(self.port))
        self.logger.debug('PATH: {}'.format(self.path))
    
    def handle(self):
        ''' Handle connection by reading data and then writing it back until EOF '''
        self.logger.debug('Handle')
        
        # Send request
        self.logger.debug('Sending request...')
        self.stream.write('GET {} HTTP/1.0\r\n'.format(self.path))
        self.stream.write('Host: {}\r\n'.format(self.host))
        self.stream.write('\r\n')
        self.stream.flush()
        
        # Receive response
        try:
            self.logger.debug('Receiving response...')
            data = self.stream.readline()
            while data:
                if(TIME == False and AVG == False):
                    sys.stdout.write(data)
                data = self.stream.readline()
        except socket.error:
            pass    # Ignore socket errors

# Main Execution

if __name__ == '__main__':
    # Parse command-line arguments
    try:
        options, arguments = getopt.getopt(sys.argv[1:], "vhp:r:ta")
    except getopt.GetoptError as e:
        usage(1)
    
    for option, value in options:
        if option == '-v':
            LOGLEVEL = logging.DEBUG
        elif option == '-h':
            usage(1)
        elif option == '-p':
            PROCESSES = int(value)
        elif option == '-r':
            REQUESTS = int(value)
        elif option == '-t':
            TIME = True
        elif option == '-a':
            AVG = True
        else:
            usage(1)

    if len(arguments) == 0:
        usage(1)
    else:
        URL = arguments[0]

    # Set logging level
    logging.basicConfig(
        level   = LOGLEVEL,
        format  = '[%(asctime)s] %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
    )
    
    # Core Control Flow
    client = HTTPClient(URL)        # Parent creates socket
    
    for process in range(PROCESSES):
        try:
            PID = os.fork()
        except OSError as e:
            print 'fork failed: {}'.format(e)
            sys.exit(1)
        
        if PID == 0:        # CHILD
            total_time = 0
            for request in range(REQUESTS):
                start_time = time.time()
                client = HTTPClient(URL)    # instantiate client
                client.run()
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                total_time += elapsed_time
                client.logger.debug('{} | Elapsed time: {:.2f}s'.format(os.getpid(), elapsed_time))
                if(TIME):
                    print '{:.3f}'.format(elapsed_time)
                
                if request == REQUESTS-1:
                    client.logger.debug('{} | Average elapsed time: {:.2f}s'.format(os.getpid(), total_time/REQUESTS))
            if(AVG):
                print '{:.3f}'.format(total_time/REQUESTS)

            os._exit(0)

    for process in range(PROCESSES):
        # Parent waits for child
        try:
            pid, status = os.wait()
        except OSError as e:    # if child interupted, parent must wait for child to finish
            if e.errno == errno.EINTR:
                pid, status = os.wait()
            else:
                print e

        client.logger.debug('Process {} terminated with exit status {} '.format(pid, status))

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: