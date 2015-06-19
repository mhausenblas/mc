#!/usr/bin/env python
"""
A simple service discovery proxy for Mesos-DNS, exposing a CORS-enabled HTTP API.
It is assumed to run on the same host as Mesos-DNS.

Usage: 

    ./sedi.py

Make sure that Mesos-DNS is installed and running, see:
http://mesosphere.github.io/mesos-dns/docs/


@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2015-06-19
@status: init
"""

import sys
import json
import urlparse
import urllib
from mc import lookup_service
from BaseHTTPServer import BaseHTTPRequestHandler

class SeDiProxy(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        logical_service_name = parsed_path.path[1:]
        self.resolve(logical_service_name)
        return
    
    def resolve(self, logical_service_name):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*') # enable CORS
        self.end_headers()
        (ip, port) = lookup_service('localhost', logical_service_name)
        self.wfile.write( 'http://' + ip + ':' + port )

################################################################################
# Main script
#
if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', 31313), SeDiProxy)
    server.serve_forever()
