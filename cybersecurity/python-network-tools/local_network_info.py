import socket
import ipaddress
from pyroute2 import IPRoute
from cidrize import cidrize

#get hostname
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)

print(hostname,IPAddr)

#list(ip_network(hostname).hosts())  
ipn = ipaddress.ip_network(IPAddr)
print(ipn.with_prefixlen)
print(ipn.with_hostmask)
print(ipn.with_netmask)
print(type(ipn.with_prefixlen))

#ips = IPRoute()
#info = [{'iface': x['index'],
 #        'addr': x.get_attr('IFA_ADDRESS'),
  #       'mask': x['prefixlen']} for x in ips.get_addr()]
#ip.close()

print(cidrize(IPAddr))