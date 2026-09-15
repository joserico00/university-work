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
TARGET_ID_CSV = "target_id.csv"
TASK_ID_CSV = "task_id.csv"


def get_scan_config_id(gmp):
    """
    Retrieve the ID of the 'Full and Fast' scan configuration.
    """
    scan_configs = gmp.get_scan_configs()
    for config in scan_configs.findall("config"):
        if config.find("name").text == "Full and fast":
            config_id = config.get("id")
            print(f"'Full and Fast' scan configuration found with ID: {config_id}")
            return config_id
    print("Failed to find 'Full and Fast' scan configuration.")
    return None


def get_scanner_id(gmp):
    """
    Retrieve the ID of the default scanner.
    """
    scanners = gmp.get_scanners()
    for scanner in scanners.findall("scanner"):
        if "OpenVAS Default" in scanner.find("name").text:
            scanner_id = scanner.get("id")
            print(f"'OpenVAS Default' scanner found with ID: {scanner_id}")
            return scanner_id
    print("Failed to find 'OpenVAS Default' scanner.")
    return None



def read_csv_to_target_list(csv_file):
    """
    Read the CSV file and extract target IDs into a list.
    """
    target_list = []
    with open(csv_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            target_list.append(row["Target ID"])
    return target_list

def save_task_id_to_csv(target_id, task_id):
    """
    Save the task ID to the task_id.csv file.
    """
    with open(TASK_ID_CSV, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([target_id, task_id])
    print(f"Saved task ID {task_id} for target ID {target_id} to {TASK_ID_CSV}")


def create_task(gmp, task_name, target_id, scan_config_id, scanner_id):
    """
    Create a task in OpenVAS.
    """
    response = gmp.create_task(
        name=task_name,
        config_id=scan_config_id,
        target_id=target_id,
        scanner_id=scanner_id
    )
    task_id = response.get("id")
    if task_id:
        print(f"Created task '{task_name}' for target ID '{target_id}' with ID: {task_id}")
    else:
        print(f"Failed to create task for target ID {target_id}. Check logs.")
    return task_id


def main():
    connection = TLSConnection(hostname=OPENVAS_HOST, port=OPENVAS_PORT)
    with Gmp(connection=connection, transform=EtreeTransform()) as gmp:
        # Authenticate with OpenVAS
        gmp.authenticate(username=USERNAME, password=PASSWORD)
        print("Authenticated with OpenVAS")

        # Get the scan configuration ID
        scan_config_id = get_scan_config_id(gmp)
        if not scan_config_id:
            print("Failed to retrieve a valid scan configuration. Exiting.")
            return

        # Get the scanner ID
        scanner_id = get_scanner_id(gmp)
        if not scanner_id:
            print("Failed to retrieve a valid scanner. Exiting.")
            return

        # Read target IDs from the target_id.csv file
        target_list = read_csv_to_target_list(TARGET_ID_CSV)
        if not target_list:
            print("No target IDs found in the CSV file. Exiting.")
            return

        print(f"Found {len(target_list)} targets to create tasks for.")

        # Process each target
        for target_id in target_list:
            print(f"Processing target ID: {target_id}")

            # Create task for the target
            task_name = f"Task for Target {target_id}"
            task_id = create_task(gmp, task_name, target_id, scan_config_id, scanner_id)
            if task_id:
                save_task_id_to_csv(target_id, task_id)
            else:
                print(f"Failed to create task for target ID {target_id}. Continuing.")


if __name__ == "__main__":
    # Ensure the task_id.csv file exists with headers
    try:
        with open(TASK_ID_CSV, "x", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Target ID", "Task ID"])  # Write headers if the file doesn't exist
    except FileExistsError:
        pass  # File already exists, no need to create

    main()
