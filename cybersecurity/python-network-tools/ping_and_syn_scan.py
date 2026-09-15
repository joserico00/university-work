import logging
import sys
from scapy.all import *
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def ping(ip):
    icmp =IP(dst=ip)/ICMP()
    resp=sr1(icmp,timeout=10)
    if resp is None:
        print("ofline")
        return False
    else:
        print("online")
        return True
        
def portsniffer(adress,firstport,lastport):
    adress=str(adress)
    firstport=int(firstport)
    lastport=int(endport)
    print("scanning ",adress," From: ",firstport,lastport)


    if firstport == lastport:
        lastport+=1

    for port in range(firstport,lastport):
        packet = IP(dst=adress)/TCP(dport=port,flags='S')
        response =sr1(packet,timeout=0.5,verbose=0)
        if response.haslayer(TCP) and response.getlayer(TCP).flags==0x12:
            print('Port '+ str(port)+ ' 'is open)
        sr(IP(dst=adress)/TCP(dport=response.sport,flags='R'),timeout=0.5,verbose=0.5)
    print('complete')