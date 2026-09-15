from scapy.all import * 
def arp_scan(ip):
    request = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip) #stack Arp on top of ethernet set to the broadcast adress
    answer,unans=srp(request, timeout=3, retry=2) 
    result =[]
    for sent,received in answer:
        result.append({'IP': received.psrc, 'MAC':received.hwsrc})
    
    return result   
for ip in arp_scan("192.168.1.57/24"):
    print (ip)
#puede estar en un network que no conteste exchange
#determinar que
#ping a cada mquina en un network
#hardware adress of all machines