import nmap3
import scapy.all as scapy
import socket
import ipaddress
request = scapy.ARP()
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
ipn = ipaddress.ip_network(IPAddr)
IPAddr="192.168.1.1"
print(IPAddr)

nmap = nmap3.Nmap()
os_results = nmap.nmap_os_detection(IPAddr)
#version_result = nmap.nmap_version_detection(IPAddr)
#print(version_result)
os_results = nmap.nmap_os_detection(IPAddr)
print(os_results)
print("Top ports")
results = nmap.scan_top_ports(IPAddr)
print(results)

results = nmap.nmap_list_scan(IPAddr)
print("listscan")
print(results)

results = nmap.nmap_subnet_scan(IPAddr)
print("subnet")
print(results)


nmapscan = nmap3.NmapScanTechniques()
result = nmapscan.nmap_tcp_scan(IPAddr)
print("Tcp scan")
print(result)

#result = nmapscan.nmap_udp_scan(IPAddr)
#print("udp scan")
#print(result)


#result = nmapscan.nmap_syn_scan(IPAddr)
#print("syn scan")
#print(result)


result = nmapscan.nmap_ping_scan(IPAddr)
print("ping scan")
print(result)

nmap = nmap3.NmapHostDiscovery()
results = nmap.nmap_arp_discovery(IPAddr)
print("host discovry")
print(result)



results = nmap.nmap_arp_discovery(IPAddr)
print("ARP discovery")
print(result)