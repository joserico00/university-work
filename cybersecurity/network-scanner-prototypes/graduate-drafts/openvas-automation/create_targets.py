import csv
from gvm.connections import TLSConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform


# OpenVAS Configuration
OPENVAS_HOST = "localhost"
OPENVAS_PORT = 9390
USERNAME = "admin"
PASSWORD = "admin"

# CSV files
ACTIVE_HOSTS_CSV = "active_hosts.csv"
TARGET_ID_CSV = "target_id.csv"


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


def target_exists(gmp, ip):
    """
    Check if a target already exists for the given IP and return its target_id if it does.
    """
    targets = gmp.get_targets()
    for target in targets.findall("target"):
        if target.find("hosts").text == ip:
            target_id = target.get("id")
            print(f"Target for IP {ip} already exists with ID: {target_id}")
            return target_id
    return None


def create_target(gmp, name, ip, port_list_id):
    """
    Create a target in OpenVAS.
    """
    response = gmp.create_target(name=name, hosts=ip, port_list_id=port_list_id)
    target_id = response.get("id")
    if target_id:
        print(f"Created target '{name}' for IP '{ip}' with ID: {target_id}")
    else:
        print(f"Failed to create target for IP {ip}. Check logs.")
    return target_id


def save_target_id_to_csv(ip, target_id):
    """
    Save the target ID to the target_id.csv file if it's not already there.
    """
    existing_data = []
    try:
        # Read existing data from the CSV
        with open(TARGET_ID_CSV, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            existing_data = list(reader)
    except FileNotFoundError:
        # If the file doesn't exist, it will be created later
        pass

    # Check if the IP is already in the CSV
    for row in existing_data:
        if row[0] == ip:
            print(f"IP {ip} already recorded in {TARGET_ID_CSV}")
            return

    # Append the new target ID to the CSV
    with open(TARGET_ID_CSV, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([ip, target_id])
    print(f"Saved target ID {target_id} for IP {ip} to {TARGET_ID_CSV}")


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

        # Read IPs from the active hosts CSV
        ip_list = read_csv_to_ip_list(ACTIVE_HOSTS_CSV)
        if not ip_list:
            print("No IPs found in the CSV file. Exiting.")
            return

        print(f"Found {len(ip_list)} active hosts.")

        # Process each IP
        for ip in ip_list:
            print(f"Processing IP: {ip}")

            # Check if target already exists
            target_id = target_exists(gmp, ip)
            if target_id:
                # Save the existing target ID to the CSV if not already recorded
                save_target_id_to_csv(ip, target_id)
                continue

            # Create target if it doesn't exist
            target_name = f"Target for {ip}"
            target_id = create_target(gmp, target_name, [ip], port_list_id)
            if target_id:
                save_target_id_to_csv(ip, target_id)
            else:
                print(f"Failed to create target for IP {ip}. Continuing.")


if __name__ == "__main__":
    # Ensure the target_id.csv file exists with headers
    try:
        with open(TARGET_ID_CSV, "x", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["IP", "Target ID"])  # Write headers if the file doesn't exist
    except FileExistsError:
        pass  # File already exists, no need to create

    main()
