import nmap
import requests
import json

# Set target IP and ports
target_ip = "192.168.0.255/24"
target_ports = "1-1024"

# Initialize nmap scanner
scanner = nmap.PortScanner()

# Scan target
print(f"Scanning {target_ip} on ports {target_ports}...")
scanner.scan(target_ip, target_ports)

# Check if target IP was scanned successfully
if target_ip not in scanner.all_hosts():
    print(f"Failed to scan {target_ip}. The host might be down or unreachable.")
    exit(1)

# Gather service information
services = []
if 'tcp' in scanner[target_ip]:
    for port in scanner[target_ip]['tcp']:
        service = scanner[target_ip]['tcp'][port]['name']
        if service not in services:
            services.append(service)
else:
    print(f"No open TCP ports found on {target_ip}.")
    exit(1)

# Query NVD for vulnerabilities
nvd_url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
vulnerabilities = []

for service in services:
    response = requests.get(f"{nvd_url}?cpeMatchString=cpe:2.3:a:*:{service.lower()}:*:*:*:*:*:*:*")
    if response.status_code == 200:
        data = json.loads(response.text)
        for cve in data["result"]["CVE_Items"]:
            vulnerabilities.append(cve["cve"]["CVE_data_meta"]["ID"])

# Print vulnerabilities
print(f"\nVulnerabilities for {target_ip}:")
for vuln in vulnerabilities:
    print(vuln)
