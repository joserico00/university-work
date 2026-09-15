import scapy.all as scapy
import socket
import ipaddress
request = scapy.ARP()
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
ipn = ipaddress.ip_network(IPAddr)
request.pdst = IPAddr+'/19'
broadcast = scapy.Ether()
  
broadcast.dst = 'ff:ff:ff:ff:ff:ff'
  
request_broadcast = broadcast / request
clients = scapy.srp(request_broadcast, timeout = 1)[0]
for element in clients:
    print(element[1].psrc + "      " + element[1].hwsrc)
    #maneras que se puede perder
    #maquina noi recive el whois
    #no responde la respuesta
    
    #PING OR BRUTEFORCE FOR FOR MACADRESS