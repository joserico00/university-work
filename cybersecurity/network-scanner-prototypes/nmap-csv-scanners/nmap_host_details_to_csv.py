import nmap
import socket
import ipaddress
import psutil
import sys
import csv
import pandas

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

    with open("scan_results.csv", "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['IP', 'Hostname', 'MAC Address', 'OS Details', 'Protocol', 'Port', 'Name', 'State', 'Product', 'Version', 'Extra Info', 'Uptime', 'Last Boot', 'Distance', 'TCP Sequence', 'IP ID Sequence', 'TCP TS Sequence', 'Vendor', 'OS Match'])

        for name, ip, netmask in ipv4_interfaces:
            network = ipaddress.IPv4Network((ip, netmask), strict=False)
            if str(network) == "127.0.0.0/8":
                continue
            print(network)
            print(f"Scanning for open ports in IP range {network} and port range {start_port}-{end_port}...")
            nm.scan(hosts=str(network), arguments=f'-p {start_port}-{end_port} -sS -O --host-timeout 10m')
            print(nm.all_hosts())
            for host in nm.all_hosts():
                hostnames = [x['name'] for x in nm[host].get('hostnames', [])]
                mac_address = nm[host]['addresses'].get('mac', 'N/A')
                os_classes = nm[host].get('osclass', [])
                os_details = ', '.join([os_class.get('osfamily', '') + ' ' + os_class.get('osgen', '') for os_class in os_classes])
                os_match =nm[host]['osmatch']
                vendor = nm[host]['vendor'].get('mac', 'N/A') if 'vendor' in nm[host] else 'N/A'
                uptime = nm[host]['uptime']['seconds'] if 'uptime' in nm[host] else 'N/A'
                lastboot = nm[host]['uptime']['lastboot'] if 'uptime' in nm[host] else 'N/A'
                distance = nm[host]['host_distance']['value'] if 'host_distance' in nm[host] else 'N/A'
                tcpsequence = nm[host]['tcpsequence']['index'] if 'tcpsequence' in nm[host] else 'N/A'
                ipidsequence = nm[host]['ipidsequence']['class'] if 'ipidsequence' in nm[host] else 'N/A'
                tcptssequence = nm[host]['tcptssequence']['class'] if 'tcptssequence' in nm[host] else 'N/A'
                for proto in nm[host].all_protocols():
                    for port in nm[host][proto]:
                        state = nm[host][proto][port]['state']
                        name = nm[host][proto][port]['name']
                        product = nm[host][proto][port]['product']
                        version = nm[host][proto][port]['version']
                        extrainfo = nm[host][proto][port]['extrainfo']   
                        #os_match = ', '.join([os_match['name'] for os_match in nm[host]['osmatches']]) if 'osmatches' in nm[host] else 'N/A'
                        csv_writer.writerow([host, ', '.join(hostnames), mac_address, os_details, proto, port, name, state, product, version, extrainfo, uptime, lastboot, distance, tcpsequence, ipidsequence, tcptssequence, vendor, os_match])

if __name__ == "__main__":
    main()
