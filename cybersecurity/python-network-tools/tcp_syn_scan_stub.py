from scapy.all import *
import socket
def tcp_scan(ip, ports):
    try:
        syn= IP(dsp=ip)/ TCP(dport=ports, flags='S')
    except:
        socket.gaierror('Hostname {} could not be resolved'.format(ip))
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)

ports = [1, 100]
tcp_scan(IPAddr, ports) 