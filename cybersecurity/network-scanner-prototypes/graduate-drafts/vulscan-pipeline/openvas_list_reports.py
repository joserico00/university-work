from gvm.connections import TLSConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform

def list_reports_by_task(gmp):
    reports = gmp.get_reports()
    print(f"📋 Found {len(reports.findall('report'))} reports in total.\n")

    for report in reports.findall("report"):
        report_id = report.get("id")
        task_elem = report.find("task")
        if task_elem is not None:
            task_id = task_elem.get("id")
            task_name = task_elem.find("name").text if task_elem.find("name") is not None else "Unnamed Task"
            print(f"📝 Report ID: {report_id}\n    ↳ Task ID: {task_id} | Name: {task_name}\n")
        else:
            print(f"📝 Report ID: {report_id}\n    ↳ No task associated\n")

def main():
    connection = TLSConnection(hostname="localhost", port=9390)
    with Gmp(connection=connection, transform=EtreeTransform()) as gmp:
        gmp.authenticate("admin", "admin")
        list_reports_by_task(gmp)

if __name__ == "__main__":
    main()

