import nmap
import socket
import ipaddress
import psutil
import sys
import requests
from bs4 import BeautifulSoup

def get_ipv4_interfaces():
    ipv4_interfaces = []

    for name, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ipv4_interfaces.append((name, addr.address, addr.netmask))

    return ipv4_interfaces

def check_vulnerabilities(product, version):
    base_url = "https://nvd.nist.gov/vuln/search/results"
    params = {
        "form_type": "Basic",
        "results_type": "overview",
        "query": f"{product} {version}",
        "search_type": "all"
    }
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    vuln_list = []

    for entry in soup.find_all("span", class_="col-md-2"):
        vuln = entry.a.text.strip()
        vuln_list.append(vuln)
    
    return vuln_list

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
            print(f"Scanning for open ports in IP range {network} and port range {start_port}-{end_port}...", file=outfile)
            if str(network) == "127.0.0.0/8":
                continue
            nm.scan(hosts=str(network), arguments=f'-p {start_port}-{end_port} -sS -O --host-timeout 10m')

            for host in nm.all_hosts():
                print(f"Full scan results for host: {host}", file=outfile)
                for protocol in nm[host].all_protocols():
                    for port in nm[host][protocol].keys():
                        service = nm[host][protocol][port]['name']
                        version = nm[host][protocol][port]['version']
                        vulnerabilities = check_vulnerabilities(service, version)
                        print(f"Service: {service}, Version: {version}, Vulnerabilities: {vulnerabilities}", file=outfile)

if __name__ == "__main__":
    main()
