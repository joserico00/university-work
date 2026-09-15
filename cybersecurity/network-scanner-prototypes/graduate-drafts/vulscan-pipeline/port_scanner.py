import nmap
import pandas as pd
from datetime import datetime
import os

def detailed_scan():
    try:
        active_hosts_df = pd.read_csv('active_hosts.csv')
    except FileNotFoundError:
        print("File active_hosts.csv not found. Please run the network discovery script first.")
        return

    nm = nmap.PortScanner()
    scan_results = []

    start_time = datetime.now()
    print(f"Scan started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    for index, row in active_hosts_df.iterrows():
        ip = row['IP']
        print(f"Scanning {ip} for open ports and services...")

        # Full port scan with service/version detection
        nm.scan(ip, arguments='-p- -T4 -A')  

        for host in nm.all_hosts():
            hostnames = [x['name'] for x in nm[host].get('hostnames', [])]
            mac_address = nm[host]['addresses'].get('mac', 'N/A')
            scan_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for proto in nm[host].all_protocols():
                for port in nm[host][proto].keys():
                    port_data = nm[host][proto][port]
                    state = port_data.get('state', 'unknown')
                    name = port_data.get('name', 'unknown')
                    product = port_data.get('product', 'unknown')
                    version = port_data.get('version', 'unknown')
                    extrainfo = port_data.get('extrainfo', '')

                    scan_results.append([
                        ip, ', '.join(hostnames), mac_address, proto, port, name, state,
                        product, version, extrainfo, scan_timestamp
                    ])

    end_time = datetime.now()
    print(f"Scan finished at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total scan duration: {end_time - start_time}")

    columns = ['IP', 'Hostname', 'MAC Address', 'Protocol', 'Port', 'Service Name', 'State', 'Product', 'Version', 'Extra Info', 'Timestamp']
    detailed_df = pd.DataFrame(scan_results, columns=columns)

    if not detailed_df.empty:
        if os.path.exists('detailed_scan_results.csv'):
            detailed_df.to_csv('detailed_scan_results.csv', mode='a', header=False, index=False)
        else:
            detailed_df.to_csv('detailed_scan_results.csv', index=False)

        print(f"Scan results saved to detailed_scan_results.csv ({len(scan_results)} entries).")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    detailed_scan()
