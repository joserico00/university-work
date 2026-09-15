import os
import requests
import csv
import time

# Your NVD API key
api_key = os.environ.get("NVD_API_KEY", "")  # set NVD_API_KEY in your environment
nvd_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Parameters for the API request
params = {
    "resultsPerPage": 100,  # Number of results per page (max is 2000)
    "startIndex": 0,        # Pagination index
}

headers = {
    "apiKey": api_key
}

# Function to fetch data from NVD and write to CSV incrementally
def fetch_and_write_vulnerabilities_to_csv():
    try:
        with open("nvd_vulnerabilities_streamed.csv", "w", newline="") as csvfile:
            fieldnames = ["CVE ID", "Description", "Reference URL", "Product Version"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Write header once

            while True:
                # Make the API request
                response = requests.get(nvd_url, params=params, headers=headers)

                # Print status code and content for debugging
                print(f"Status Code: {response.status_code}")
                print(f"Response Content: {response.content}")

                # Check for valid response
                if response.status_code != 200:
                    print(f"Error: Received non-200 response: {response.status_code}")
                    break

                data = response.json()

                # If no results or an error, stop the loop
                if "vulnerabilities" not in data or not data["vulnerabilities"]:
                    print("No vulnerabilities found or empty response.")
                    break

                # Loop through each vulnerability and write directly to the CSV file
                for item in data["vulnerabilities"]:
                    cve_id = item["cve"]["id"]
                    description = item["cve"]["descriptions"][0]["value"]
                    reference_url = item["cve"]["references"][0]["url"] if item["cve"]["references"] else "N/A"
                    product_version = (
                        item["cve"]["affects"]["vendor"]["vendor_data"][0]["product"]["product_data"][0]["version"]["version_data"][0]["version_value"]
                        if "affects" in item["cve"] and item["cve"]["affects"]["vendor"]["vendor_data"]
                        else "N/A"
                    )

                    # Write the vulnerability data directly to the CSV file
                    writer.writerow({
                        "CVE ID": cve_id,
                        "Description": description,
                        "Reference URL": reference_url,
                        "Product Version": product_version
                    })

                # Update the start index for the next page of results
                params["startIndex"] += params["resultsPerPage"]

                # Respect NVD rate limit (sleep for 1 second between requests)
                time.sleep(1)

        print("Vulnerabilities saved to nvd_vulnerabilities_streamed.csv")

    except Exception as e:
        print(f"Error fetching vulnerabilities: {e}")

# Main execution
if __name__ == "__main__":
    print("Fetching vulnerabilities from NVD API...")
    fetch_and_write_vulnerabilities_to_csv()
