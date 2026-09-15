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
TASK_ID_CSV = "task_id.csv"
REPORT_CSV = "task_reports.csv"
CONSOLIDATED_REPORT = "consolidated_reports.csv"

def get_report_by_task_id(gmp, task_id):
    """
    Search for the report by task ID in all reports.
    """
    reports = gmp.get_reports()
    for report in reports.findall("report"):
        if report.find("task").get("id") == task_id:
            return report.get("id")
    return None


def get_task_status(gmp, task_id):
    """
    Check the status of a task in OpenVAS and return its report ID if available.
    """
    try:
        task = gmp.get_task(task_id=task_id)
        if task is None:
            print(f"Task ID {task_id} not found in OpenVAS.")
            return None, None

        # Get task status
        status = task.find("task").find("status").text

        # Try to fetch report ID
        report_element = task.find("task").find("last_report")
        report_id = report_element.get("id") if report_element is not None else None

        # Fallback to searching all reports
        if report_id is None and status == "Done":
            print(f"No 'last_report' found for task ID {task_id}. Searching all reports...")
            report_id = get_report_by_task_id(gmp, task_id)

        return status, report_id
    except Exception as e:
        print(f"Error retrieving status or report for task ID {task_id}: {e}")
        return None, None

def generate_report(gmp, task_id):
    """
    Generate a report for a completed task in OpenVAS.
    """
    task = gmp.get_task(task_id=task_id)
    report_id = task.find("task").find("last_report").get("id")
    
    if not report_id:
        print(f"No report found for task ID: {task_id}")
        return None

    # Get the report in CSV format
    report = gmp.get_report(report_id=report_id, report_format_id="c1645568-627a-11e3-a660-406186ea4fc5")
    report_content = report.find("report").text

    # Save the report to a file
    report_file = f"report_{task_id}.csv"
    with open(report_file, "w") as file:
        file.write(report_content)
    print(f"Saved report for task ID {task_id} to {report_file}")
    return report_file


def append_to_consolidated_csv(task_id, report_file):
    """
    Append the contents of a report file to the consolidated CSV.
    """
    with open(report_file, "r") as infile:
        reader = csv.reader(infile)
        with open(CONSOLIDATED_REPORT, "a", newline="") as outfile:
            writer = csv.writer(outfile)
            for row in reader:
                writer.writerow([task_id] + row)  # Add Task ID as the first column
    print(f"Appended report for task ID {task_id} to {CONSOLIDATED_REPORT}")


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


def save_task_report_csv(task_id, report_file):
    """
    Save the task report information to the report CSV file.
    """
    with open(REPORT_CSV, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([task_id, report_file])
    print(f"Recorded report for task ID {task_id} in {REPORT_CSV}")


def main():
    connection = TLSConnection(hostname=OPENVAS_HOST, port=OPENVAS_PORT)
    with Gmp(connection=connection, transform=EtreeTransform()) as gmp:
        # Authenticate with OpenVAS
        gmp.authenticate(username=USERNAME, password=PASSWORD)
        print("Authenticated with OpenVAS")

        # Ensure the report CSV has headers
        try:
            with open(REPORT_CSV, "x", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Task ID", "Report File"])
        except FileExistsError:
            pass

        # Ensure the consolidated CSV has headers
        try:
            with open(CONSOLIDATED_REPORT, "x", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Task ID", "Host", "Port", "Vulnerability", "Severity"])
        except FileExistsError:
            pass

        # Read task IDs from the task_id.csv file
        task_list = read_csv_to_task_list(TASK_ID_CSV)
        if not task_list:
            print("No task IDs found in the CSV file. Exiting.")
            return

        print(f"Found {len(task_list)} tasks to check and generate reports.")

        # Check status and generate report for each task
        for task_id in task_list:
            print(f"Processing Task ID: {task_id}")
            status, report_id = get_task_status(gmp, task_id)

            if status == "Done" and report_id:
                print(f"Task {task_id} is completed with Report ID: {report_id}")
                report_file = generate_report(gmp, report_id)
                if report_file:
                    save_task_report_csv(task_id, report_file)
                    append_to_consolidated_csv(task_id, report_file)
            elif status == "Done" and not report_id:
                print(f"Task {task_id} is marked as Done but has no valid report.")
            else:
                print(f"Task {task_id} is not completed yet. Skipping.")

if __name__ == "__main__":
    main()

