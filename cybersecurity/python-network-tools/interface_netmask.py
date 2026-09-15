import netifaces
import ipaddress
print(netifaces.interfaces() )
addrs =  netifaces.ifaddresses('en0') 
print(addrs)

print(addrs[netifaces.AF_INET] )
hIp=addrs[netifaces.AF_INET][0]
ip=hIp['addr']
netmask=hIp['netmask']
broadcast=hIp['broadcast']
print(ipaddress.IPv4Network(broadcast + "/"+ netmask, strict=False).prefixlen)