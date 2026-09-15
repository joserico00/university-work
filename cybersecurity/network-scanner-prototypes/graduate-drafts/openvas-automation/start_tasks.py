import csv
from gvm.connections import TLSConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform


# OpenVAS Configuration
OPENVAS_HOST = "localhost"
OPENVAS_PORT = 9390
USERNAME = "admin"
PASSWORD = "admin"

# CSV file
TASK_ID_CSV = "task_id.csv"


def start_task(gmp, task_id):
    """
    Start a task in OpenVAS.
    """
    try:
        gmp.start_task(task_id=task_id)
        print(f"Started task with ID: {task_id}")
    except Exception as e:
        print(f"Failed to start task with ID {task_id}. Error: {e}")


def read_csv_to_task_list(csv_file):
    """
    Read the CSV file and extract task IDs into a list.
    """
    task_list = []
    with open(csv_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            task_list.append(row["Task ID"])
    return task_list


def main():
    connection = TLSConnection(hostname=OPENVAS_HOST, port=OPENVAS_PORT)
    with Gmp(connection=connection, transform=EtreeTransform()) as gmp:
        # Authenticate with OpenVAS
        gmp.authenticate(username=USERNAME, password=PASSWORD)
        print("Authenticated with OpenVAS")

        # Read task IDs from the task_id.csv file
        task_list = read_csv_to_task_list(TASK_ID_CSV)
        if not task_list:
            print("No task IDs found in the CSV file. Exiting.")
            return

        print(f"Found {len(task_list)} tasks to start.")

        # Start each task
        for task_id in task_list:
            start_task(gmp, task_id)


if __name__ == "__main__":
    main()

