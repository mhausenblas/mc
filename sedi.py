#!/usr/bin/env python
"""
A simple service discovery proxy for Mesos-DNS, exposing a CORS-enabled HTTP API.

Usage: 

    ./sedi.py $MESOS_DNS_HOST

Make sure that Mesos-DNS is installed and running, see:
http://mesosphere.github.io/mesos-dns/docs/

Example: 

    ./sedi.py localhost

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2015-06-19
@status: init
"""

import sys
import json
import urlparse
import urllib
from BaseHTTPServer import BaseHTTPRequestHandler

class SeDiProxy(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        logical_service_name = parsed_path.path[1:]
        self.resolve(logical_service_name)
        return
    
    def resolve(self, logical_service_name):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') # enable CORS - http://enable-cors.org/#how
        self.end_headers()
        self.wfile.write(lookup_service('localhost', logical_service_name))

################################################################################
# Main script
#
if __name__ == '__main__':
    try:
        from BaseHTTPServer import HTTPServer
        server = HTTPServer(('localhost', 31313), SeDiProxy)
        server.serve_forever()
    except err:
        print(err)
        print(__doc__)
        sys.exit(2)