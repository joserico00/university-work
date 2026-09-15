import nmap
import pandas as pd
from datetime import datetime

def detailed_scan():
    try:
        active_hosts_df = pd.read_csv('active_hosts.csv')
    except FileNotFoundError:
        print("File active_hosts.csv not found. Please run the network discovery script first.")
        return

    nm = nmap.PortScanner()
    scan_results = []

    for index, row in active_hosts_df.iterrows():
        ip = row['IP']
        print(f"Scanning {ip} for detailed information...")
        nm.scan(ip, arguments='-p- -sV -O --script=default -T4 --open -A --host-timeout 10m -v')

        for host in nm.all_hosts():
            hostnames = [x['name'] for x in nm[host].get('hostnames', [])]
            mac_address = nm[host]['addresses'].get('mac', 'N/A')
            os_classes = nm[host].get('osclass', [])
            os_details = ', '.join([os_class.get('osfamily', '') + ' ' + os_class.get('osgen', '') for os_class in os_classes])
            scan_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for proto in nm[host].all_protocols():
                for port in nm[host][proto]:
                    state = nm[host][proto][port]['state']
                    name = nm[host][proto][port]['name']
                    product = nm[host][proto][port]['product']
                    version = nm[host][proto][port]['version']
                    extrainfo = nm[host][proto][port]['extrainfo']
                    row = [ip, ', '.join(hostnames), mac_address, os_details, proto, port, name, state, product, version, extrainfo, scan_timestamp]
                    scan_results.append(row)

    columns = ['IP', 'Hostname', 'MAC Address', 'OS Details', 'Protocol', 'Port', 'Name', 'State', 'Product', 'Version', 'Extra Info', 'Timestamp']
    detailed_df = pd.DataFrame(scan_results, columns=columns)
    detailed_df.to_csv('detailed_scan_results.csv', index=False)

    print(detailed_df)

if __name__ == "__main__":
    detailed_scan()
