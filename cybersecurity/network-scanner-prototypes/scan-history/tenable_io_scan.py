import os
from tenable.io import TenableIO

def run_scan(target_ip):
    # Create a Tenable.io client
    tio = TenableIO(os.environ['TIO_ACCESS_KEY'], os.environ['TIO_SECRET_KEY'])  # set these environment variables with your Tenable.io API keys

    # Define the scan settings
    scan_settings = {
        'name': 'pratice scan',
        'text_targets': target_ip,
        'enabled': True,
        'launch': 'ON_DEMAND',
    }

    # Create the scan
    scan = tio.scans.create(
        settings=scan_settings,
        credentials=[os.environ['SCAN_USERNAME'], os.environ['SCAN_PASSWORD']],  # scan credentials from environment variables
        plugins={}
    )

    # Launch the scan
    scan_id = scan['id']
    tio.scans.launch(scan_id)

    # Wait for the scan to complete (use a better waiting mechanism in production)
    import time
    while tio.scans.status(scan_id) != 'completed':
        time.sleep(60)  # Sleep for 1 minute

    # Export the scan results to a file
    with open('scan_results.nessus', 'wb') as file:
        tio.scans.export(scan_id, fobj=file)

if __name__ == "__main__":
    target_ip = '192.168.1.1'  # Adjust this to your target IP
    run_scan(target_ip)
