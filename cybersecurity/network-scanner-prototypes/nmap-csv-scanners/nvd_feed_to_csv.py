import requests
import json
import csv
import gzip
from io import BytesIO

year = 2020
url = f"https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{year}.json.gz"

response = requests.get(url)
compressed_file = BytesIO(response.content)
decompressed_file = gzip.GzipFile(fileobj=compressed_file)

data = json.loads(decompressed_file.read().decode("utf-8"))

# Extract CVE items
cve_items = data["CVE_Items"]

# Save to CSV
with open(f"cve_dataset_{year}.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    # Write headers
    writer.writerow(["CVE ID", "Published Date", "Description", "Impact Score V3", "Impact Score V2", "CPEs"])
    for item in cve_items:
        cve_id = item["cve"]["CVE_data_meta"]["ID"]
        pub_date = item["publishedDate"]
        description = item["cve"]["description"]["description_data"][0]["value"]
        impact_score_v3 = item.get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("baseScore", "N/A")
        impact_score_v2 = item.get("impact", {}).get("baseMetricV2", {}).get("cvssV2", {}).get("baseScore", "N/A")

        writer.writerow([cve_id, pub_date, description, impact_score_v3, impact_score_v2])

print(f"Dataset for {year} saved to cve_dataset_{year}.csv")
