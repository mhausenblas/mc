#!/usr/bin/env python
"""
The Mesos-DNS Client

Usage: 

    ./mc.py $MESOS_DNS_HOST $SERVICE_NAME

Make sure that Mesos-DNS is installed and running, see:
http://mesosphere.github.io/mesos-dns/docs/

Example: 

    ./mc.py localhost flask.marathon.mesos 

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2015-06-01
@status: init
"""

import sys
import os
import logging
import urllib2
import json
import random


################################################################################
# Config
#
DEBUG = True
MESOS_DNS_PORT = 8123

################################################################################
# Global vars
#

if DEBUG:
    FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')
else:
    FORMAT = '%(asctime)-0s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')

def lookup_service(mesosdns_server, service_name):
    mesosdns_endpoint = 'http://' + mesosdns_server + ':' + str(MESOS_DNS_PORT)
    logging.debug('Discovery of service %s using %s' %(service_name, mesosdns_endpoint))
    components = service_name.split('.')
    lookup = '_' + components[0] + '._tcp.' + '.'.join(str(x) for x in components[1:])
    logging.debug('Looking up: %s ' %(lookup))
    payload = json.load(urllib2.urlopen(mesosdns_endpoint + '/v1/services/' + lookup + '.'))
    service_instance = random.choice(payload)
    return (service_instance['ip'], service_instance['port'])

################################################################################
# Main script
#
if __name__ == '__main__':
    try:
        (ip, port) = lookup_service(sys.argv[1], sys.argv[2])
        print 'Discovered %s running on %s:%s' %(sys.argv[2], str(ip), str(port))
    except err:
        print(err)
        print(__doc__)
        sys.exit(2)
