import nmap
import socket
import ipaddress
import psutil
import sys
import pandas as pd
from datetime import datetime

def get_ipv4_interfaces():
    ipv4_interfaces = []

    for name, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ipv4_interfaces.append((name, addr.address, addr.netmask))

    return ipv4_interfaces

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <start_port> <end_port>")
        sys.exit(1)

    start_port = int(sys.argv[1])
    end_port = int(sys.argv[2])

    ipv4_interfaces = get_ipv4_interfaces()

    if not ipv4_interfaces:
        print("No active IPv4 network interfaces found.")
        sys.exit(1)

    nm = nmap.PortScanner()
    scan_results = []

    for name, ip, netmask in ipv4_interfaces:
        network = ipaddress.IPv4Network((ip, netmask), strict=False)
        if str(network) == "127.0.0.0/8":
            continue

        print(f"Scanning for open ports in IP range {network} and port range {start_port}-{end_port}...")
        nm.scan(hosts=str(network), arguments=f'-p- -sS -O -T4')

        for host in nm.all_hosts():
            mac_address = nm[host]['addresses'].get('mac', 'N/A')

            for proto in nm[host].all_protocols():
                for port in nm[host][proto]:
                    state = nm[host][proto][port]['state']
                    row = [host, port, mac_address]
                    scan_results.append(row)

    columns=['IP', 'Port', 'MAC Address']
    df = pd.DataFrame(scan_results, columns=columns)

    try:
        with open('scan_results.csv', 'x', newline='') as file:
            pd.DataFrame(columns=columns).to_csv(file, index=False)
    except FileExistsError:
        pass
    
    with open('scan_results.csv', 'a', newline='') as file:
        df.to_csv(file, header=False, index=False)

    print(df)

if __name__ == "__main__":
    main()

