import nmap
import socket
import ipaddress
import psutil
import sys

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

    for name, ip, netmask in ipv4_interfaces:
        network = ipaddress.IPv4Network((ip, netmask), strict=False)
        print(f"Scanning for open ports in IP range {network} and port range {start_port}-{end_port}...")
        print(network)
        if str(network)== "127.0.0.0/8":
            continue
        
        nm.scan(hosts=str(network), arguments=f'-p {start_port}-{end_port}')

        for host in nm.all_hosts():
            print(f"Host: {host} ({nm[host].hostname()})")
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                print(f"Protocol: {proto}")
                print(f"Ports: {', '.join(map(str, sorted(ports)))}")

if __name__ == "__main__":
    main()