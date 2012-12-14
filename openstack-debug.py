import os
import sys
from xmlrpclib import ServerProxy
import re

'''
__author__="David Busby"
__copyright__="David Busby <oneiroi@fedoraproject.org>"
__license__="GNU v3 + part 5d section 7: Redistribution/Reuse of this code is permitted under the GNU v3 license, as an additional term ALL code must carry the original Author(s) credit in comment form."
'''

def main():
  rSanitize=re.compile('(sql_connection.*\=|password.*\=).*')
  log_buff_size=102400
  nova_logs=[
    '/var/log/nova/api.log',
    '/var/log/nova/cert.log',
    '/var/log/nova/compute.log',
    '/var/log/nova/consoleauth.log',
    '/var/log/nova/network.log',
    '/var/log/nova/nova-dhcpbridge.log',
    '/var/log/nova/nova-manage.log',
    '/var/log/nova/nova-network.log',
    '/var/log/nova/objectstore.log',
    '/var/log/nova/scheduler.log',
    '/var/log/nova/volume.log',
  ]
  nova_configs=[
    '/etc/nova/api-paste.ini', 
    '/etc/nova/nova.conf', 
    '/etc/nova/policy.json', 
  ]
  a = raw_input('This script will send your logs and config files for openstack to paste.openstack.org; passwords and sql_connection lines are redacted.\n\nAre you sure you wish to continue? (y/n):')
  while a.lower() not in ('y','n'):
      a = raw_input('Invalid response, please specify y or n:')
  if a == 'n':
      print 'Aborting on user request'
      sys.exit(1)
  
  novaSTR = ''
  for c in nova_configs:
    if not os.path.isfile(c):
      print 404,c
    else:
      novaSTR += "=== %s ===\n\n" % c
      try:
        f = open(c)
        buff = ''
        for line in f:
          if rSanitize.search(line):
            buff += rSanitize.sub("\\1 ***REDACTED**",line) 
          else:
            buff += line
        novaSTR += buff
      except OSError, e:
         novaSTR += "OSError %s" %e

  for l in nova_logs:
    if not os.path.isfile(l):
      print 404,l
    else:
      novaSTR += "=== %s ===\n\n" % l
      try:
        f = open(l)
        s = sys.getsizeof(l)
        buff = ''
        if (s - log_buff_size) > 0:
          f.seek(s - log_buff_size)
          for line in f:
            buff += line
        novaSTR += buff
      except OSError, e:
         novaSTR += "OSError %s" %e

      
  header = "Output generated by openstack-debug.py (https://github.com/Oneiroi/openstack-debug) if there is a problem with the output please raise an issue!\n\n"
  s = ServerProxy('http://paste.openstack.org/xmlrpc/')
  id = s.pastes.newPaste('en',"%s%s"%(header,novaSTR))
  print 'http://paste.openstack.org/show/%s/' % id

if __name__ == '__main__':
  main()
