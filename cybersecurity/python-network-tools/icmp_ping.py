import sys
from scapy.all import *
print("ping")  
ip= sys.argv[1]
icmp =IP(dst=ip)/ICMP()
resp=sr1(icmp,timeout=10)
if resp is None:
    print("ofline")
else:
    print("online")