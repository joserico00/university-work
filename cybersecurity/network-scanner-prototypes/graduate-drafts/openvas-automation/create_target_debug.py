import csv
from gvm.connections import TLSConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
# import xml.etree.ElementTree as ET

# OpenVAS Configuration
OPENVAS_HOST = "localhost"
OPENVAS_PORT = 9390
USERNAME = "admin"
PASSWORD = "admin"

# CSV file containing active hosts
CSV_FILE = "active_hosts.csv"


def get_port_list_id(gmp):
    """
    Retrieve a valid port list ID.
    """
    port_lists = gmp.get_port_lists()
    default_port_list_id = None
    for port_list in port_lists.findall("port_list"):
        name = port_list.find("name").text
        port_list_id = port_list.get("id")
        print(f"Port List: {name} (ID: {port_list_id})")
        if "OpenVAS Default" in name:
            default_port_list_id = port_list_id

    # If "OpenVAS Default" is not found, use the first available port list
    if not default_port_list_id and port_lists:
        default_port_list_id = port_lists.find("port_list").get("id")
        print(f"'OpenVAS Default' not found. Using the first available port list with ID: {default_port_list_id}")

    return default_port_list_id

def create_target(gmp, name, hosts, port_list_id):
    # Ensure proper formatting of the host list
    hosts_str = ",".join(host.strip() for host in hosts)  # Remove whitespace
    response = gmp.create_target(name=name, hosts=hosts_str, port_list_id=port_list_id)
    
    # Debug: Print the raw XML response
    response_xml = response
    print(f"Raw XML Response:\n{response_xml}")

    target_id = response.get("id")
    if target_id:
        print(f"Created target '{name}' for IPs '{hosts_str}' with ID: {target_id}")
    else:
        print("Failed to create target. Check response and logs.")
    return target_id

def read_csv_to_ip_list(csv_file):
    """
    Read the CSV file and extract IPs into a list.
    """
    ip_list = []
    with open(csv_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ip_list.append(row["IP"])
    return ip_list


def main():
    connection = TLSConnection(hostname=OPENVAS_HOST, port=OPENVAS_PORT)
    with Gmp(connection=connection, transform=EtreeTransform()) as gmp:
        # Authenticate with OpenVAS
        gmp.authenticate(username=USERNAME, password=PASSWORD)
        print("Authenticated with OpenVAS")

        # Get a valid port list ID
        port_list_id = get_port_list_id(gmp)
        if not port_list_id:
            print("Failed to retrieve a valid port list. Exiting.")
            return

        # Read IPs from CSV
        ip_list = read_csv_to_ip_list(CSV_FILE)
        if not ip_list:
            print("No IPs found in the CSV file. Exiting.")
            return
        test_hosts = ip_list[:2]  # Use the first two IPs for testing
        print(f"Using test hosts: {test_hosts}")

        print(f"Found {len(ip_list)} active hosts: {ip_list}")

        # Create a target with the active hosts
        target_name = "Active Hosts Target"
        target_id = create_target(gmp, target_name, test_hosts, port_list_id)
        if not target_id:
            print("Failed to create target. Exiting.")
            return

        print(f"Target created successfully with ID: {target_id}")


if __name__ == "__main__":
    main()
