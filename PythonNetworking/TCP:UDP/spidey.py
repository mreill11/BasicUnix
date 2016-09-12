#!/usr/bin/env python2.7

import getopt
import logging
import os
import socket
import sys
import mimetypes
import signal

# Constants

ADDRESS  = '0.0.0.0'
PORT     = 9234
BACKLOG  = 0
DOCROOT = 'www'
FORK = False
LOGLEVEL = logging.INFO
PROGRAM  = os.path.basename(sys.argv[0])

# Utility Functions

def usage(exit_code=0):
    print >>sys.stderr, '''Usage: spidey.py [-d DOCROOT -p PORT -f -v]
        
        Options:
        
        -h         Show this help message
        -f         Enable forking mode
        -v         Set logging to DEBUG level
        
        -d DOCROOT Set root directory (default is current directory)
        -p PORT    TCP Port to listen to (default is 9234)
        '''.format(port=PORT, program=PROGRAM)
    sys.exit(exit_code)

# BaseHandler Class

class BaseHandler(object):
    
    def __init__(self, fd, address):
        ''' Construct handler from file descriptor and remote client address '''
        self.logger  = logging.getLogger()        # Grab logging instance
        self.socket  = fd                         # Store socket file descriptor
        self.address = '{}:{}'.format(*address)   # Store address
        self.stream  = self.socket.makefile('w+') # Open file object from file descriptor
        
        self.debug('Connect')
    
    def debug(self, message, *args):
        ''' Convenience debugging function '''
        message = message.format(*args)
        self.logger.debug('{} | {}'.format(self.address, message))
    
    def info(self, message, *args):
        ''' Convenience information function '''
        message = message.format(*args)
        self.logger.info('{} | {}'.format(self.address, message))
    
    def warn(self, message, *args):
        ''' Convenience warning function '''
        message = message.format(*args)
        self.logger.warn('{} | {}'.format(self.address, message))
    
    def error(self, message, *args):
        ''' Convenience error function '''
        message = message.format(*args)
        self.logger.error('{} | {}'.format(self.address, message))
    
    def exception(self, message, *args):
        ''' Convenience exception function '''
        message = message.format(*args)
        self.logger.error('{} | {}'.format(self.address, message))
    
    def handle(self):
        ''' Handle connection '''
        self.debug('Handle')
        raise NotImplementedError
    
    def finish(self):
        ''' Finish connection by flushing stream, shutting down socket, and
            then closing it '''
        self.debug('Finish')
        try:
            self.stream.flush()
            self.socket.shutdown(socket.SHUT_RDWR)
        except socket.error as e:
            pass    # Ignore socket errors
        finally:
            self.socket.close()

# HTTPHandler Class

class HTTPHandler(BaseHandler):
    def __init__(self, fd, address, docroot=None):
        BaseHandler.__init__(self, fd, address)
    
    def handle(self):
        ''' Handle connection by reading data and then writing it back until EOF '''
        
        # Parse HTTP request and headers
        self._parse_request()
        
        # Build uripath by normalizing REQUEST_URI
        self.docroot = DOCROOT  # WHERE SHOULD WE PUT THIS
        self.uripath = os.path.normpath(self.docroot + os.environ['REQUEST_URI'])
        
        # Check path existence and types and then dispatch
        if not os.path.exists(self.uripath) or not self.uripath.startswith(self.docroot):
            self._handle_error(404) # 404 error
        elif os.path.isfile(self.uripath) and os.access(self.uripath, os.X_OK):
            self._handle_script()   # CGI script
        elif os.path.isfile(self.uripath) and os.access(self.uripath, os.R_OK):
            self._handle_file()     # Static file
        elif os.path.isdir(self.uripath) and os.access(self.uripath, os.R_OK):
            self._handle_directory()# Directory listing
        else:
            self._handler_error(403)# 403 error

    def _parse_request(self):
    
        # Parse the TCP Connection Address
        os.environ['REMOTE_ADDR'] = self.address.split(':',1)[0]
        os.environ['REMOTE_HOST'] = ADDRESS
        os.environ['REMOTE_PORT'] = str(PORT)
        
        # Parse first line of HTTP Request
        data = self.stream.readline().strip().split()
        self.debug('Parsing {}'.format(data))
    
        os.environ['REQUEST_METHOD'] = data[0]
        os.environ['REQUEST_URI'] = data[1].split('?')[0]
        os.environ['QUERY_STRING'] = data[1].split('?')[-1]
    
        # Parse additional lines of HTTP Request, convert them to appropriate format, add to environment
        data = self.stream.readline().strip().split(': ')
        while data:
            KEY = 'HTTP_' + data[0].upper().replace('-', '_')
            VALUE = data[1]
            os.environ[KEY] = VALUE
            data = self.stream.readline().strip().split(': ')
            if len(data) is 1:
                break

    def _handle_error(self, error_code):
    
        self.debug('Handle Error')
        # Send HTTP Status code for the request
        # Send content type
        self.stream.write('HTTP/1.0 404 NOT FOUND\r\n')
        self.stream.write('Content-Type: text/html\r\n')
        self.stream.write('\r\n')
    
        self.stream.write('''<!DOCTYPE html>
            <html lang="en">
            <head>
            <title>404 Error</title>
            <link href="https://www3.nd.edu/~pbui/static/css/blugold.css" rel="stylesheet">
            <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css" rel"stylesheet">
            </head>
            <body>
            <div class="container">
            <div class="page-header">
            <h2>404 Error</h2>
            </div>
            <div class="thumbnail">
            <img src="{}" class="img-responsive">
            </div>
            </div>
            </body>
            </html>'''.format('https://media.giphy.com/media/26AHLBZUC1n53ozi8/giphy.gif'))
    
    def _handle_script(self):
        
        self.debug('Handle Script')
        
        # Set SIGCHLD to Default
        signal.signal(signal.SIGCHLD, signal.SIG_DFL)
        
        for line in os.popen(self.uripath):
            # write line to socket
            self.stream.write(line)
            self.stream.flush()
        
        # Set SIGCHLD to Ignore
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    def _handle_file(self):
    
        self.debug('Handle File')
        
        # Guess mimetype
        mimetype, _ = mimetypes.guess_type(self.uripath)
        if mimetype is None:
            mimetype = 'application/octet-stream'
    
        self.stream.write('HTTP/1.0 200 OK\r\n')
        self.stream.write('Content-Type: {}\r\n'.format(mimetype))
        self.stream.write('\r\n')
        
        #self.stream.write('<p>')
        
        for line in open(self.uripath, 'r+b'):
            #self.stream.write('<p>')
            self.stream.write(line)
            #self.stream.write('</p>')
            self.stream.flush()

    def _handle_directory(self):
    
        self.debug('Handle Directory')
        
        self.stream.write('HTTP/1.0 200 OK\r\n')
        self.stream.write('Content-Type: text/html\r\n')
        self.stream.write('\r\n')
        
        # HTML Header
        self.stream.write('''<!DOCTYPE html>
            <html lang="en">
            <head>
            <title>/</title>
            <link href="https://www3.nd.edu/~pbui/static/css/blugold.css" rel="stylesheet">
            <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css" rel="stylesheet">
            </head>
            <body>
            <div class="container">
            <div class="page-header">
            <h2>Directory Listing: {}</h2>
            </div>
            <table class="table table-striped">
            <thead>
            <th>Type</th>
            <th>Name</th>
            <th>Size</th>
            </thead>
            <tbody>'''.format('/'+self.uripath.split('/')[-1]))
        
        # HTML Body
        for entry in os.listdir(self.uripath):
            if os.path.isdir(self.uripath+'/'+entry):
                # The HREF should be os.environ['REQUEST_URI'] + entry
                HREF = os.environ['REQUEST_URI'] +'/'+ entry
                HREF = HREF.replace('//','/')
                self.stream.write('''<tr>
                    <td><i class="fa fa-folder-o"></i></td>
                    <td><a href="{}">{}</a></td>
                    <td>-</td>
                    </tr>'''.format( HREF, entry))
        for entry in os.listdir(self.uripath):
            if os.path.isfile(self.uripath+'/'+entry):
                HREF = os.environ['REQUEST_URI'] +'/' +entry
                HREF = HREF.replace('//','/')
                self.stream.write('''<tr>
                    <td><i class="fa fa-file-o"></i></td>
                    <td><a href="{}">{}</a></td>
                    <td>{}</td>
                    </tr>'''.format( HREF, entry, os.path.getsize(self.uripath+'/'+entry)))
    
        # HTML End
        self.stream.write('''</tbody>
            </table>
            </div>
            </body>
            </html>''')

def _handler_error(self):
    self.debug('Handler Error')

# TCPServer Class

class TCPServer(object):
    
    def __init__(self, address=ADDRESS, port=PORT, forking=FORK, handler=HTTPHandler):
        ''' Construct TCPServer object with the specified address, port, and
            handler '''
        self.logger  = logging.getLogger()                              # Grab logging instance
        self.socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Allocate TCP socket
        self.address = address                                          # Store address to listen on
        self.port    = port                                             # Store port to lisen on
        self.forking = forking                                          # Sets boolean forking variable
        self.handler = handler                                          # Store handler for incoming connections
    
    def run(self):
        ''' Run TCP Server on specified address and port by calling the
            specified handler on each incoming connection '''
        try:
            # Bind socket to address and port and then listen
            self.socket.bind((self.address, self.port))
            self.socket.listen(BACKLOG)
        except socket.error as e:
            self.logger.error('Could not listen on {}:{}: {}'.format(self.address, self.port, e))
            sys.exit(1)
        
        self.logger.info('Listening on {}:{}...'.format(self.address, self.port))
        
        # Ignore Children
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        
        while True:
            # Accept incoming connection
            self.client, self.address = self.socket.accept()
            self.logger.debug('Accepted connection from {}:{}'.format(*self.address))
            
            if not self.forking:
                # Instantiate handler, handle connection, finish connection
                try:
                    handler = self.handler(self.client, self.address)
                    handler.handle()
                except Exception as e:
                    handler.exception('Exception: {}', e)
                finally:
                    handler.finish()
            else:
                # Fork process
                pid = os.fork()
                
                if pid == 0:    # CHILD
                    # Instantiate handler, handle connection, finish connection
                    try:
                        handler = self.handler(self.client, self.address)
                        handler.handle()
                    except Exception as e:
                        handler.exception('Exception: {}', e)
                    finally:
                        handler.finish()
                        os._exit(0)
                else:
                    self.client.close()

# Main Execution

if __name__ == '__main__':
    # Parse command-line arguments
    try:
        options, arguments = getopt.getopt(sys.argv[1:], "hfvd:p:")
    except getopt.GetoptError as e:
        usage(1)
    
    for option, value in options:
        if option == '-h':
            usage(1)
        elif option == '-f':
            FORK = True
        elif option == '-v':
            LOGLEVEL = logging.DEBUG
        elif option == '-d':
            DOCROOT = value
        elif option == '-p':
            PORT = int(value)
        else:
            usage(1)

    # Set logging level
    logging.basicConfig(
        level   = LOGLEVEL,
        format  = '[%(asctime)s] %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
    )
    
    # Instantiate and run server
    server = TCPServer(address=ADDRESS, port=PORT, forking=FORK, handler=HTTPHandler)
    
    try:
        server.run()
    except KeyboardInterrupt:
        sys.exit(0)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python: