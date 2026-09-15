import nmap
import psutil
import socket
import ipaddress
import pandas as pd
from datetime import datetime

def get_ipv4_interfaces():
    ipv4_interfaces = []
    for name, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ipv4_interfaces.append((name, addr.address, addr.netmask))
    return ipv4_interfaces

def network_discovery():
    ipv4_interfaces = get_ipv4_interfaces()
    if not ipv4_interfaces:
        print("No active IPv4 network interfaces found.")
        return

    nm = nmap.PortScanner()
    active_hosts = []

    for name, ip, netmask in ipv4_interfaces:
        network = ipaddress.IPv4Network((ip, netmask), strict=False)
        if str(network) == "127.0.0.0/8":
            continue

        print(f"Discovering hosts in IP range {network}...")
        nm.scan(hosts=str(network), arguments='-sn -T4 --open')
        
        for host in nm.all_hosts():
            active_hosts.append([host, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    columns = ['IP', 'Discovery Timestamp']
    df = pd.DataFrame(active_hosts, columns=columns)
    df.to_csv('active_hosts.csv', index=False)

if __name__ == "__main__":
    network_discovery()
