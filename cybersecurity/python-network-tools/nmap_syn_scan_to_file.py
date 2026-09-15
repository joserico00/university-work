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

    with open("scan_results.txt", "w") as outfile:
        for name, ip, netmask in ipv4_interfaces:
            network = ipaddress.IPv4Network((ip, netmask), strict=False)
            if str(network)== "127.0.0.0/8":
                continue
            print(network)
            print(f"Scanning for open ports in IP range {network} and port range {start_port}-{end_port}...", file=outfile)
            nm.scan(hosts=str(network), arguments=f'-p {start_port}-{end_port} -sS --host-timeout 10m')

            for host in nm.all_hosts():
                if 'hostnames' in nm[host]:
                    hostnames = [x['name'] for x in nm[host]['hostnames']]
                else:
                    hostnames = []

                if 'addresses' in nm[host]:
                    mac_address = nm[host]['addresses'].get('mac', 'N/A')
                else:
                    mac_address = 'N/A'

                if 'osclass' in nm[host]:
                    os_classes = nm[host]['osclass']
                    os_details = ', '.join([os_class.get('osfamily', '') + ' ' + os_class.get('osgen', '') for os_class in os_classes])
                else:
                    os_details = 'N/A'
                    
                print(f"Host: {host} ({', '.join(hostnames)})", file=outfile)
                print(f"MAC Address: {mac_address}", file=outfile)
                print(f"OS Details: {os_details}", file=outfile)

                for proto in nm[host].all_protocols():
                    open_ports = [port for port in nm[host][proto].keys() if nm[host][proto][port]['state'] == 'open']
                    if open_ports:
                        print(f"Protocol: {proto}", file=outfile)
                        print(f"Open Ports: {', '.join(map(str, sorted(open_ports)))}", file=outfile)
                print("",file=outfile)
if __name__ == "__main__":
    main()