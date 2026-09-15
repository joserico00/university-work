import logging
import sys
from scapy.all import *
import socket
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
##   print("use: tsrget startport endport")
  #  sys.exit()


#get hostname
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)

#adress=str(sys.argv[1])
adress=IPAddr
#firstport=int(sys.argv[2])
#lastport=int(sys.argv[3])
firstport=1
lastport=10
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

#CHEKIANDO PU
#PRIMERO PING
#DESPUES PUEDES CHEKIAR EL ARP
#SI EXISTE CHEKIAR LOS PUERTOS
