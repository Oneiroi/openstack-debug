import os
import sys
from xmlrpclib import ServerProxy

'''
__author__="David Busby"
__copyright__="David Busby <d.busby@saiweb.co.uk>"
__license__="GNU v3 + part 5d section 7: Redistribution/Reuse of this code is permitted under the GNU v3 license, as an additional term ALL code must carry the original Author(s) credit in comment form."
'''

def main():
    a = raw_input('This script will send your logs and config files for openstack to paste.openstack.org, are you sure you wish to continue? (y/n):')
    while a.lower() not in ('y','n'):
        a = raw_input('Invalid response, please specify y or n:')
    if a == 'n':
        print 'Aborting on user request'
        sys.exit(1)
    novaConf = None
    if not os.path.isfile('/etc/nova/nova.conf'):
        print '404 /etc/nova/nova.conf'
    else:
        try:
            f = open('/etc/nova/nova.conf')
            novaConf = f.read()
        except OSError, e:
            print 'Error reading nova.conf',e
    novaLog = None
    if not os.path.isfile('/var/log/nova/nova.log'):
        print '404 /var/log/nova/nova.log'
    else:
        try:
            f = open('/var/log/nova/nova.log')
            novaLog = f.read()
        except OSError, e:
            print 'Error reading nova.log',e
    if novaConf and novaLog:
        novaSTR = "Output generated by openstack-debug.py (https://github.com/Oneiroi/openstack-debug)\n\n===== nova.conf =====\n%s\n\n===== nova.log =====\n%s\n\n" % (novaConf,novaLog)
        s = ServerProxy('http://paste.openstack.org/xmlrpc/')
        id = s.pastes.newPaste('en',novaSTR)
        print 'http://paste.openstack.org/show/%s/' % id
    else:
        print 'Some required data was missing I will not push to paste.openstack.org'
        
if __name__ == '__main__':
    main()
