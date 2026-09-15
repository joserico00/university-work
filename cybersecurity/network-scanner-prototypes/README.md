# Network Scanner Prototypes

Prototypes and drafts written on the way to [NVSRCO](https://github.com/joserico00/NVSRCO), my graduate project on automated network vulnerability scanning and reporting. The code starts with single-file nmap scanners that write a CSV, then adds timestamped scan history and Plotly Dash dashboards, and ends with a multi-stage pipeline. That pipeline discovers hosts, port-scans them, runs vulnerability checks (OpenVAS/GVM over GMP, the `vulscan` NSE script, a self-hosted CVE-Search instance, the NVD API), and visualizes the results. The code is kept as it was written, including unfinished drafts and near-duplicates, as a record of how the design evolved. Scan results are generated at runtime and are not included in the repository.

> **Legal / ethical use.** These scripts scan every subnet the host is attached to, run intrusive nmap profiles (`-A`, NSE scripts, OS detection), and launch OpenVAS/Tenable scans. Only run them against networks and systems you own or have explicit written authorization to test.

## How it works

Most scanners start the same way. `psutil.net_if_addrs()` lists the machine's IPv4 interfaces, `ipaddress.IPv4Network((ip, netmask), strict=False)` turns each one into its subnet (skipping `127.0.0.0/8`), and python-nmap's `PortScanner.scan()` scans that subnet. Results are walked host → protocol → port, and the service fields (`state`, `name`, `product`, `version`, `extrainfo`) are collected into rows.

The later drafts in `graduate-drafts/` split this into stages that pass data to each other through CSV files in the current working directory:

```
local IPv4 interfaces (psutil + ipaddress)
   |
   v
[1] Host discovery        network_discovery.py         nmap -sn
   |                      -> active_hosts.csv
   |
   +------------------------------------------------------+
   |                                                      |
   v                                                      v
[2] Port scan             port_scanner.py            [3c] OpenVAS / GVM over GMP (TLS, port 9390)
    nmap -p- (-T4 -A)                                    create_targets.py  -> target_id.csv
    -> detailed_scan_results.csv                         create_tasks.py      -> task_id.csv
   |                                                     start_tasks.py
   +------------------------------+                      get_reports.py   -> report_<task>.csv
   |                              |                                           consolidated_reports.csv
   v                              v
[3a] nmap + vulscan NSE     [3b] self-hosted CVE-Search API
     vulnerability_scan.py       cve_lookup_by_product.py / cve_lookup_by_vendor.py
     -> vulnerability_scan_      -> vulnerabilities.csv
        results.csv

[4] Dashboard   dashboard.py (Plotly Dash, http://127.0.0.1:8050)
                reads data/scan_results.csv   (port-scan rows with a Timestamp column)
                  and data/openvasscan.csv    (an OpenVAS "CSV Results" report)
```

The folders roughly follow that progression:

| Folder | Role |
|---|---|
| `nmap-csv-scanners/` | One-shot nmap scans of every local subnet, saved to CSV (one variant also saves to SQLite), plus an NVD feed downloader. |
| `scan-history/` | Adds a `Timestamp` column and append-only CSV output so repeated runs build a history. Also has a more intrusive nmap profile and a Tenable.io draft. |
| `dashboards/` | Plotly Dash dashboards over the scan history and an OpenVAS CSV export. |
| `graduate-drafts/` | The staged pipeline: discovery → port scan → vulnerability checks (OpenVAS, vulscan, CVE-Search, NVD) → extended dashboard. Includes a Docker-packaged OpenVAS version. |

```
network-scanner-prototypes/
├── nmap-csv-scanners/
├── scan-history/
├── dashboards/
│   └── drafts/
└── graduate-drafts/
    ├── vulscan-pipeline/   tidied nmap pipeline stages (1, 2, 3a)
    ├── openvas-automation/               OpenVAS pipeline + Docker + dashboard (stage 3c, 4)
    │   └── Docker/
    ├── local-cve-search/            CVE-Search API lookups (stage 3b)
    ├── nvd-database/                NVD CVE API 2.0 -> CSV
    └── cve-search-nmap/                  nmap -sV + CVE-Search lookup in one script
```

## Files

### `nmap-csv-scanners/`

`nmap_scan_to_csv.py`, `nmap_scan_to_sqlite.py`, and `nmap_host_details_to_csv.py` share the same core:

1. They require two positional arguments, `<start_port> <end_port>` (`sys.argv`), and print a usage message otherwise.
2. `get_ipv4_interfaces()` → subnet per interface, skipping loopback.
3. They run `nm.scan(hosts=<subnet>, arguments="-p <start>-<end> -sS -O --host-timeout 10m")`. That is a SYN scan with OS detection, so **root is required**.
4. For each host they collect hostnames, MAC address, and per-port `state`, `name`, `product`, `version`, `extrainfo`.

| File | What differs | Output |
|---|---|---|
| `nmap_scan_to_csv.py` | Builds rows `IP Range, IP, Hostname, MAC Address, OS Details, Protocol, Port, Name, State, Product, Version, Extra Info` into a pandas DataFrame and prints it. | `scan_results.csv` (overwritten) |
| `nmap_scan_to_sqlite.py` | Same scan without the `IP Range` column. It also opens a SQLite database file named `networklogs` (no extension), creates a `network` table, and writes the DataFrame with `to_sql(..., if_exists="replace")`, so each run replaces the table. | `scan_results.csv` (overwritten) and the SQLite file `networklogs` |
| `nmap_host_details_to_csv.py` | Writes rows with the `csv` module as it scans, and adds host-level columns: `Uptime`, `Last Boot`, `Distance`, `TCP Sequence`, `IP ID Sequence`, `TCP TS Sequence`, `Vendor`, and `OS Match` (python-nmap's raw `osmatch` list). | `scan_results.csv` (overwritten) |

**`nvd_feed_to_csv.py`** does no scanning. It downloads the NVD JSON 1.1 yearly feed for a hardcoded `year = 2020` (`nvdcve-1.1-2020.json.gz`), decompresses it in memory with `gzip`/`BytesIO`, and writes one row per CVE: `CVE ID`, `Published Date`, `Description`, and the CVSS v3 and v2 base scores (labelled "Impact Score"). The header also has a `CPEs` column, but no value is written for it. Output: `cve_dataset_2020.csv`. The JSON 1.1 feeds are a legacy NVD data source.

### `scan-history/`

Despite the folder name, none of these scripts call the `vulscan` NSE script. That happens in `graduate-drafts/vulscan-pipeline/vulnerability_scan.py`.

**`nmap_scan_history.py`** is the `nmap_scan_to_csv.py` flow (same arguments, `-sS -O --host-timeout 10m`, same columns) plus a `Timestamp` column. Instead of overwriting, it creates `scan_results.csv` with a header only if the file doesn't exist (`open(..., "x")`), then **appends** the new rows. Running it repeatedly builds the scan history that the dashboards in `dashboards/` read. It also prints the DataFrame.

**`nmap_intrusive_scan_history.py`** writes the same output format as `nmap_scan_history.py` (appended `scan_results.csv`). It still requires the two port arguments, but the nmap arguments are hardcoded to `-p- -sV -O --script=default -T4 --open -A --host-timeout 10m -v`: all 65,535 TCP ports, version detection, default NSE scripts, OS detection, and open ports only. The port arguments only appear in the printed message. It also prints each host's raw python-nmap result dict. It is much slower and noisier than the other scanners, and it needs root.

**`tenable_io_scan.py`** is a draft for Tenable.io (cloud Nessus) using `pytenable`. `run_scan(target_ip)` creates a `TenableIO` client from the API access key and secret key in the **`TIO_ACCESS_KEY` and `TIO_SECRET_KEY` environment variables** (no keys are stored in the file, and a missing variable raises `KeyError`), calls `tio.scans.create()` with a settings dict (`name`, `text_targets`, `launch: ON_DEMAND`) and scan credentials read from the **`SCAN_USERNAME` and `SCAN_PASSWORD` environment variables**, launches the scan, polls `tio.scans.status()` every 60 seconds until it returns `completed`, and exports the result to `scan_results.nessus`. The target is set with `target_ip` in `__main__`. The keyword arguments passed to `scans.create()` don't appear to match pytenable's documented interface, so treat this as an untested draft. It requires a Tenable.io account, API keys exported as `TIO_ACCESS_KEY` and `TIO_SECRET_KEY`, and scan credentials exported as `SCAN_USERNAME` and `SCAN_PASSWORD`.

### `dashboards/`

Both dashboards in this folder load their data from the current directory when the script starts:

- `scan_results.csv`: timestamped nmap output from `nmap_scan_history.py` or `nmap_intrusive_scan_history.py`. The dashboards use the `IP` and `Timestamp` columns.
- `openvasscan.csv`: an OpenVAS/GVM report exported in "CSV Results" format. The columns used are `IP`, `NVT Name`, `Severity`, `CVSS`, `Summary`, and `Solution Type`.

**`scan_dashboard.py`** is the working dashboard in this folder. It runs `app.run_server(debug=True)` at `http://127.0.0.1:8050` and has three tabs:

1. **IP Table**: a dropdown of scan timestamps (defaults to the latest). The `update_table` callback takes the selected timestamp and the one immediately before it, shows the rows from both, and adds a `Status` column: **New** (IP only in the selected scan), **Existing** (in both), or **Gone** (only in the previous scan). Rows are colored blue, green, or red, with grey for Unknown, and a legend explains the colors. Native sort and filter are enabled. The IP sets are also printed to the console.
2. **Timeline Graph**: `px.line` of unique IPs per scan timestamp.
3. **Vulnerability Analysis**: OpenVAS findings grouped by `IP`, `NVT Name`, and `Severity`, shown as a `px.treemap` (IP → NVT name) that is sized and colored by CVSS. Hovering shows CVSS, severity, summary, and solution type. Severity and IP dropdowns filter the treemap. Clicking a tile shows the finding's details and links to the other IPs with the same NVT; clicking one of those links filters the treemap to that IP.

**`readme.txt`** holds the original run notes: install `dash`, run `scan_dashboard.py`, open `http://127.0.0.1:8050`.

#### `dashboards/drafts/`

Earlier iterations that `scan_dashboard.py` combines:

| File | What it is | State |
|---|---|---|
| `treemap_draft_v1.py` | First treemap draft. Severity and IP dropdowns, a treemap colored by severity with an explicit green/yellow/red map, and click-for-details with related IP links. | **Does not start.** `State` and `json` are used without being imported. One callback lists an input component (`ip-list-output`) that isn't in the layout and passes four inputs to a three-parameter function, and the string `'ALL'` is used instead of Dash's `ALL` wildcard. |
| `treemap_draft_v2.py` | Treemap draft where related-IP clicks are handled inside `update_treemap` through a pattern-matching `{'type': 'dynamic-ip', 'index': ALL}` input. Colors come from a precomputed `Severity Color` column. | Runnable draft. It became the Vulnerability Analysis tab. |
| `treemap_draft_v2_copy.py` | Near-identical copy of `treemap_draft_v2.py`. | **Does not parse:** the first line starts with a stray tab, and the `Details` f-string is split across two lines. |
| `tabbed_layout_draft.py` | First attempt at the tabbed layout: the IP Table tab (timestamp dropdown, New/Existing/Gone logic, legend), the Timeline Graph tab, and an empty placeholder "Tab 3". | **Incomplete.** `update_table()` never returns, because its `return` ended up after a different function. The treemap callbacks reference components and variables (`grouped_data`, `vulnerability_data`) that don't exist in this file. |

### `graduate-drafts/` (top level)

**`network_discovery.py`** is stage 1. It takes no arguments. For each non-loopback subnet it runs `nm.scan(hosts=<subnet>, arguments="-sn -T4 --open")`, a ping scan with no port scan, and records every host nmap returns along with a discovery timestamp. Output: `active_hosts.csv` (`IP, Discovery Timestamp`), overwritten each run. Identical copies are in `local-cve-search/` and `openvas-automation/`.

**`port_scanner.py`** is stage 2. It reads `active_hosts.csv` (and prints a hint if the file is missing), then runs `nm.scan(ip, arguments="-p- -T5")` on each IP. That covers all TCP ports at nmap's fastest timing template. There is no `-sV`, so `Product` and `Version` usually come back empty. For each port it records `IP, Hostname, MAC Address, Protocol, Port, Name, State, Product, Version, Extra Info, Timestamp`, and it prints the start time, end time, and total duration. Output: `detailed_scan_results.csv`, appended; the header is written only when the file is first created. An identical copy is in `openvas-automation/`, and the `local-cve-search/` copy uses `-p- -T4 -A` instead.

**`port_scanner_detailed.py`** is an earlier variant of `port_scanner.py`. It reads the same input, uses `-p- -sV -O --script=default -T4 --open -A --host-timeout 10m -v`, adds an `OS Details` column, and **overwrites** `detailed_scan_results.csv`. It has no timing output and needs root.

**`subnet_port_mac_scan.py`** requires `<start_port> <end_port>` but ignores them. For each local subnet it runs `-p- -sS -O -T4` (root) and records only `IP, Port, MAC Address`; it reads the port state but doesn't store it. Output: appended to `scan_results.csv`, with the header written on first creation.

**`openvas_create_target.py`** creates an OpenVAS scan target; it doesn't run nmap. It connects to gvmd over GMP/TLS (`TLSConnection`, `localhost:9390`) and authenticates with the `USERNAME`/`PASSWORD` constants at the top of the file. It then lists port lists and picks the one whose name contains "OpenVAS Default" (or the first one), reads every IP from `active_hosts.csv`, and creates a single target, "Active Hosts Target", containing all of them. It prints the response and the target ID. The IPs are joined into a comma-separated string before `gmp.create_target(hosts=...)` is called, but python-gvm expects a list and joins it itself, so the host list is likely malformed. `openvas-automation/create_targets.py` passes a list instead.

**`openvas_gmp_connection_test.py`** is a GMP smoke test. It connects over TLS to `localhost:9390`, authenticates, and prints `gmp.get_version()` and `gmp.get_tasks()`. With `EtreeTransform` these print as lxml element objects, not XML text. Any exception is printed.

**`openvas_scan_skeleton.py`** is a **skeleton, not a working scan**. It reads `active_hosts.csv`, opens GMP over `UnixSocketConnection()` (the default gvmd socket), and authenticates with the literal placeholder strings `'username'` / `'password'`. `initiate_scan()` and `get_scan_results()` are stubs that return fixed values (`"scan_id_for_<ip>"`, severity `Medium`, `5` vulnerabilities). It writes those placeholder values to `openvas_scan_results.csv` (`IP, Severity, Vulnerabilities`).

**`dashboard.py`** extends the `scan_dashboard.py` dashboard. It reads `data/scan_results.csv` and `data/openvasscan.csv` relative to the working directory. The scan CSV needs `IP`, `Port`, and `Timestamp` columns (the `port_scanner.py` format). It serves on `http://127.0.0.1:8050` with `debug=True` and has two tabs:

- **Overview**: a `RangeSlider` over the scan timestamps drives a single callback that updates:
  - the scan table for the selected range, where every row gets the status "Within Range";
  - unique IPs per **day** (`px.line`);
  - a bar chart of port frequencies in the range;
  - a severity pie chart (from the whole OpenVAS file, not filtered by the slider);
  - an IP × Port heatmap (`pd.crosstab` + `go.Heatmap`);
  - an IP-change bar chart and table (Added / Removed / Existing, compared with the scan just before the range start);
  - a summary section: total unique IPs, total findings, the highest-CVSS NVT, the most common NVT, the most common IP, the average CVSS, the top 5 ports, and the top 5 IPs by finding count.
- **Vulnerability Analysis**: the same treemap, filters, and related-IP links as `scan_dashboard.py`.

**`xor_decode_exercise.py`** has nothing to do with scanning; it is a capture-the-flag exercise. The first part takes a hardcoded integer array modulo 256 and decodes it with a rolling XOR key (`y = (y * 3) % 256 + 6`), printing the results as a "Registry Path" and a "Registry Key Name". The second part base64-decodes a hardcoded pickled game save, prints it, sets `health` and `attack` to 1000, and re-pickles and re-encodes it. The re-encoded string is left as a bare expression (notebook style), so it isn't printed when the file runs as a script. It uses `numpy`. `pickle.loads` is only safe here because the input is a fixed string.

### `graduate-drafts/vulscan-pipeline/`

Tidied versions of the nmap-based stages.

**`network_discovery.py`** is stage 1, like the top-level version, but it runs `-sn -T4` (no `--open`). It writes `active_hosts.csv` only if at least one host was found, and prints the count.

**`port_scanner.py`** is stage 2. It reads `active_hosts.csv` and runs `-p- -T4 -A` on each host: all ports plus version detection, OS detection, default scripts, and traceroute, so it needs root. Port fields are read with `.get()` defaults (`"unknown"`), and the service column is named `Service Name`. It appends to `detailed_scan_results.csv` only when there are results, and prints the start time, end time, and duration.

**`vulnerability_scan.py`** is stage 3a. It reads `detailed_scan_results.csv`, and for **each row** runs `nmap -sV --script=vulscan/vulscan.nse -p <port> <ip>`. For each port in the result it takes the `vulscan` script output from `port_data["script"]["vulscan"]` (or `"No vulnerabilities found"`) and records `IP, Port, Protocol, Service, State, Vulnerabilities, Timestamp`, where `Vulnerabilities` is the raw vulscan text. Output: `vulnerability_scan_results.csv`, appended. It prints the start time, end time, and duration. Because it runs once per CSV row, duplicate rows (for example from repeated, appended port scans) are scanned again. It requires the vulscan NSE script to be installed.

**`openvas_list_reports.py`** is a GMP helper. It connects to `localhost:9390`, authenticates with credentials written inline, and lists every report with its task ID and task name.

### `graduate-drafts/local-cve-search/`

Stage 3b experiments against a **self-hosted CVE-Search instance** (the open-source cve-search project's web API) at `https://localhost`. All requests use `verify=False`, which suits a local deployment with a self-signed certificate.

| File | What it does | Inputs | Outputs |
|---|---|---|---|
| `network_discovery.py` | Identical to `graduate-drafts/network_discovery.py`. | – | `active_hosts.csv` |
| `port_scanner.py` | Same as `graduate-drafts/port_scanner.py`, but with `-p- -T4 -A`, so `Product` and `Version` get filled in, which the lookups below need. | `active_hosts.csv` | `detailed_scan_results.csv` (appended) |
| `cve_lookup_by_product.py` | Skips rows that lack `Product` or `Version`, requests `GET /api/search/<product>/<version>`, and turns each entry of the response's `cves` list into `IP, Port, Product, Version, CVE_ID, Description, CVSS_Score`. CVE-Search's search route is `/api/search/<vendor>/<product>`, so nmap's product and version strings end up in the vendor and product slots, and matches are unlikely without mapping them to CPE names first. | `detailed_scan_results.csv` | `vulnerabilities.csv` (overwritten) |
| `cve_lookup_by_product_quiet.py` | The same logic as `cve_lookup_by_product.py`. The only differences are that it suppresses urllib3's `InsecureRequestWarning` and has different comments. | `detailed_scan_results.csv` | `vulnerabilities.csv` |
| `cve_lookup_by_vendor.py` | Vendor/product variant: `GET /api/browse/<vendor>/<product>`. The vendor comes from a `Vendor` column if one exists, otherwise it's `"unknown"`; the port-scan CSV has no such column, so it is always `"unknown"`. Only `Product` is required. Rows: `IP, Port, Vendor, Product, CVE_ID, Description, CVSS_Score`. | `detailed_scan_results.csv` | `vulnerabilities.csv` |
| `export_all_cves.py` | Dumps CVEs from the local instance. It requests `/api/cves?page=N` starting at 0 until it gets an empty `cves` list, a non-200 status, or an exception, and writes `CVE_ID, Description, CVSS_Score, Published_Date, Modified_Date` as it goes. | none | `cve_dataset.csv` |
| `cve_search_api_probe.py` | Two API probes: `/api/cve/<id>` for a sample CVE ID and `/api/browse/microsoft/windows_10`. Prints the JSON. | none | console |
| `pycvesearch_probe.py` | The same kind of probe using `pycvesearch`: `CVESearch("https://localhost", verify=False).search("microsoft/windows_10")`, printing each result. A `version` variable only appears in the messages; despite the comment, nothing is filtered by version. | none | console |

### `graduate-drafts/nvd-database/`

**`nvd_api_to_csv.py`** downloads CVEs from the **NVD CVE API 2.0** (`services.nvd.nist.gov/rest/json/cves/2.0`) into a CSV.

- **API key:** read from the **`NVD_API_KEY` environment variable** (`os.environ.get("NVD_API_KEY", "")`) and sent as the `apiKey` request header. If the variable isn't set, an empty key is sent. You can request a key from NVD; it raises the rate limit.
- **How it works:** it pages with `resultsPerPage=100`, adding 100 to `startIndex` after each page and sleeping 1 second between requests. It stops on a non-200 response or an empty `vulnerabilities` array. For each CVE it writes the ID, the first description, and the first reference URL (or `N/A`). Rows are written as each page arrives.
- **Output:** `nvd_vulnerabilities_streamed.csv` (`CVE ID, Description, Reference URL, Product Version`). The status code and the **full raw response body** of every page are printed, so console output is very large.
- **Notes:** `Product Version` is read from an `affects` key that belongs to the older NVD JSON schema and isn't in API 2.0 responses, so that column is always `N/A`. Downloading the full NVD catalogue takes thousands of requests at 100 results per page.

### `graduate-drafts/cve-search-nmap/`

**`nmap_cve_search.py`** uses the cve-search API. `scan_network()` runs `nmap -sV` against a hardcoded `/24`, which you can change with the `target_network` variable in `__main__`. For each port with a non-empty `product`, `get_cves()` requests `https://localhost/api/cvefor/<product>:<version>` (`verify=False`), and `display_cves()` prints each result's `id` and `summary`. All output goes to the console. The `cvefor` endpoint expects a CPE string, so the raw `product:version` string from nmap may not match anything.

### `graduate-drafts/openvas-automation/`

A packaged version of the OpenVAS pipeline: Docker setup, discovery and port scan, GMP automation, and the latest dashboard revision. Run order: `network_discovery.py` → `port_scanner.py` → `create_targets.py` → `create_tasks.py` → `start_tasks.py` → `get_reports.py` → `dashboard.py`.

All GMP scripts connect with `TLSConnection(hostname="localhost", port=9390)`, wrap the connection in `Gmp(..., transform=EtreeTransform())`, and authenticate with the `USERNAME`/`PASSWORD` constants at the top of each file. Those constants match the default lab credentials set in `Docker/docker-compose.yml`.

**`Docker/Dockerfile`** starts `FROM immauss/openvas` (a community all-in-one OpenVAS/GVM image), installs `python3`, `python3-pip`, and `nmap` with apt, `EXPOSE`s 9390, and starts with `CMD ["/usr/local/bin/start"]`.

**`Docker/docker-compose.yml`** builds that Dockerfile as the service and container `openvas`. It publishes `9392` (web UI) and `9390` (GMP), sets the `USERNAME`/`PASSWORD` environment variables for the admin account, mounts `./GBCommunitySigningKey.asc` to `/etc/GBCommunitySigningKey.asc`, and uses `restart: unless-stopped`. That mount path is relative to `Docker/`, but the key file is one level up in `openvas-automation/`. Depending on the base image version, gvmd may also need extra configuration to accept GMP connections on TCP 9390; publishing the port alone may not be enough.

**`GBCommunitySigningKey.asc`** is a PGP **public** key block (named for the Greenbone Community Feed signing key) that the Compose file mounts into the container.

**`network_discovery.py`, `port_scanner.py`** are identical to the top-level `graduate-drafts/` versions (`-sn -T4 --open`; `-p- -T5`).

**`create_targets.py`** is stage 3c, step 1.

- It creates `target_id.csv` with the header `IP, Target ID` if the file doesn't exist, then logs in and picks a port list (one containing "OpenVAS Default", otherwise the first).
- For each IP in `active_hosts.csv`, `target_exists()` looks through all existing targets for one whose `hosts` equals that IP, and reuses its ID if found. Otherwise it calls `create_target(name="Target for <ip>", hosts=[ip], port_list_id=...)`.
- `save_target_id_to_csv()` appends `IP, Target ID` unless that IP is already in the file, so re-runs don't create duplicates.

**`create_tasks.py`** is step 2. It finds the scan config named exactly `Full and fast` and the scanner whose name contains `OpenVAS Default`. For each `Target ID` in `target_id.csv` it creates the task `Task for Target <id>` and appends `Target ID, Task ID` to `task_id.csv` (creating the header if needed). There is no duplicate check, so running it again creates another task for each target.

**`start_tasks.py`** is step 3. It reads every `Task ID` from `task_id.csv` and calls `gmp.start_task()` on each, printing any errors per task.

**`get_reports.py`** is step 4.

- It creates `task_reports.csv` (`Task ID, Report File`) and `consolidated_reports.csv` (`Task ID, Host, Port, Vulnerability, Severity`) if they don't exist.
- For each task in `task_id.csv`, `get_task_status()` reads the task status and its `last_report` ID, falling back to searching all reports for that task.
- For tasks with status `Done`, `generate_report()` requests the report in OpenVAS's CSV Results report format (`report_format_id="c1645568-627a-11e3-a660-406186ea4fc5"`), saves it as `report_<id>.csv`, records it in `task_reports.csv`, and appends its rows, prefixed with the task ID, to `consolidated_reports.csv`. Unfinished tasks are skipped, so you run the script again later.
- **Known issues:**
  - `main()` passes the *report* ID to `generate_report()`, which treats its argument as a *task* ID and calls `get_task()` with it, so the report step fails as written.
  - GMP returns non-XML report formats base64-encoded, and the script writes the element text without decoding it.
  - The consolidated header doesn't match the columns of an OpenVAS CSV report.

**`create_target_debug.py`** is a debugging version of target creation. It works like `graduate-drafts/openvas_create_target.py`, but strips whitespace and uses only the **first two** IPs from `active_hosts.csv` to create one "Active Hosts Target".

**`dashboard.py`** is the latest dashboard revision. It reads the same `data/scan_results.csv` and `data/openvasscan.csv`. Compared with `graduate-drafts/dashboard.py`:

- The Overview table's `Status` column is rendered as Markdown and holds emoji badges ("Added", "Removed", "Still Active"), computed against the scan just before the selected range.
- Placeholder rows are appended for removed IPs so they still appear in the table.
- The IP-change chart and table say "Still Active" instead of "Existing".
- The new conditional row styles (green or red left border) filter on the plain labels, but the `Status` values carry an emoji prefix, so those styles never match.

**`notes.txt`** and **`README_OpenVAS_Project.md`** are the original setup notes: install Nmap and Docker, the pip packages, the Docker commands, the run order, and the expected files. Some names in them differ from the code:

- The notes say `port_scanner.py` writes `ports.csv`; it actually writes `detailed_scan_results.csv`.
- The `nmap` import comes from the `python-nmap` package.

Where the notes and this README differ, this README matches the code.

**`task_reports.csv`** contains only the header row that `get_reports.py` creates. There are no results in it.

`dashboard.py` expects `data/scan_results.csv` and `data/openvasscan.csv` in a `data/` folder next to it (not included; create it and add your own exports).

## Requirements

- **Python 3.6+.** f-strings are used throughout, and there is no Python 2 code. Use a current Python 3 release to work with current pandas, Dash, and python-gvm.
- **Python packages** (inferred from the imports):

  | Package | Used for |
  |---|---|
  | `python-nmap` (imported as `nmap`) | every nmap-based scanner |
  | `psutil` | interface/subnet detection |
  | `pandas` | CSV/DataFrame handling in scanners, lookups, and dashboards |
  | `requests`, `urllib3` | NVD, CVE-Search API calls |
  | `python-gvm` (imported as `gvm`; also pulled in by `gvm-tools`) | all OpenVAS/GMP scripts |
  | `dash` **2.x**, `plotly` | dashboards (`app.run_server()` was removed in Dash 3) |
  | `pycvesearch` | `local-cve-search/pycvesearch_probe.py` |
  | `pytenable` (imported as `tenable`) | `scan-history/tenable_io_scan.py` |
  | `numpy` | `graduate-drafts/xor_decode_exercise.py` |

  `csv`, `sqlite3`, `gzip`, `json`, `ipaddress`, `socket`, and `datetime` are in the standard library.

- **External tools and services:**
  - **nmap** on `PATH`. python-nmap calls the binary.
  - **Root / sudo** for the nmap profiles that use `-sS`, `-O`, or `-A`: `nmap-csv-scanners/*` scanners, `scan-history/nmap_scan_history.py` and `nmap_intrusive_scan_history.py`, `graduate-drafts/subnet_port_mac_scan.py` and `port_scanner_detailed.py`, and the `-A` versions of `port_scanner.py` in `vulscan-pipeline/` and `local-cve-search/`. `-sn` discovery runs without root, but it only uses ARP on the local segment as root, so the original notes run discovery and port scanning with `sudo`.
  - **vulscan NSE script** (scipag/vulscan), installed so that `vulscan/vulscan.nse` resolves in nmap's scripts directory, for `vulnerability_scan.py`.
  - **OpenVAS / GVM** with gvmd reachable over TLS at `localhost:9390`, for example the container in `openvas-automation/Docker/`. `openvas_scan_skeleton.py` uses the local gvmd Unix socket instead. On first start the feed sync takes a long time; the original notes allow about 30 minutes.
  - **Docker and Docker Compose** for the OpenVAS container.
  - **CVE-Search** served at `https://localhost`, for `local-cve-search/` and `cve-search-nmap/`.
  - **NVD API key** in the `NVD_API_KEY` environment variable, for `nvd-database/nvd_api_to_csv.py`.
  - **Tenable.io account and API keys** in the `TIO_ACCESS_KEY` and `TIO_SECRET_KEY` environment variables, plus `SCAN_USERNAME` and `SCAN_PASSWORD`, for `tenable_io_scan.py`.

## Usage

Every script reads and writes files relative to the **current working directory**, so run each one from its own folder.

```bash
pip install python-nmap psutil pandas requests "dash<3" plotly python-gvm pycvesearch
```

**Single-run subnet scans**

```bash
cd nmap-csv-scanners
sudo python3 nmap_scan_to_csv.py 1 1024        # -> scan_results.csv
sudo python3 nmap_scan_to_sqlite.py 1 1024          # -> scan_results.csv + SQLite file "networklogs"
sudo python3 nmap_host_details_to_csv.py 1 1024           # -> scan_results.csv with extra host columns
python3 nvd_feed_to_csv.py                     # -> cve_dataset_2020.csv
```

**Scan history + dashboard**

```bash
cd scan-history
sudo python3 nmap_scan_history.py 1 1024     # run several times; appends to scan_results.csv

# Copy scan_results.csv into dashboards/, and export an OpenVAS report in
# "CSV Results" format there as openvasscan.csv
cd ../dashboards
python3 scan_dashboard.py          # open http://127.0.0.1:8050
```

**nmap-only pipeline (stages 1 → 2 → 3a)**

```bash
cd graduate-drafts/vulscan-pipeline
sudo python3 network_discovery.py          # -> active_hosts.csv
sudo python3 port_scanner.py               # -> detailed_scan_results.csv
python3 vulnerability_scan.py             # -> vulnerability_scan_results.csv (needs vulscan)
```

**CVE-Search lookups (stage 3b)**, with a CVE-Search instance running at `https://localhost`:

```bash
cd graduate-drafts/local-cve-search
sudo python3 network_discovery.py
sudo python3 port_scanner.py
python3 cve_lookup_by_product.py               # -> vulnerabilities.csv
python3 export_all_cves.py                         # -> cve_dataset.csv (full dump from the local instance)
```

**OpenVAS pipeline and dashboard (stages 1 → 3c → 4)**

```bash
cd graduate-drafts/openvas-automation/Docker
docker compose up -d --build              # first start: wait for the feed sync to finish
cd ..
sudo python3 network_discovery.py          # -> active_hosts.csv
sudo python3 port_scanner.py               # -> detailed_scan_results.csv
python3 create_targets.py                  # -> target_id.csv
python3 create_tasks.py                      # -> task_id.csv
python3 start_tasks.py
python3 get_reports.py                   # re-run until tasks report Done

mkdir -p data
cp detailed_scan_results.csv data/scan_results.csv
# export a finished OpenVAS report as "CSV Results" to data/openvasscan.csv
python3 dashboard.py                         # open http://127.0.0.1:8050
```

**NVD API 2.0 download**

```bash
export NVD_API_KEY="your-nvd-api-key"
cd graduate-drafts/nvd-database
python3 nvd_api_to_csv.py                    # -> nvd_vulnerabilities_streamed.csv
```

**Other single scripts**

```bash
python3 graduate-drafts/openvas_gmp_connection_test.py        # check GMP connectivity
python3 graduate-drafts/vulscan-pipeline/openvas_list_reports.py     # list OpenVAS reports by task
python3 graduate-drafts/cve-search-nmap/nmap_cve_search.py              # edit target_network first
```

**Tenable.io draft**

```bash
export TIO_ACCESS_KEY="your-access-key" TIO_SECRET_KEY="your-secret-key" SCAN_USERNAME="scan-user" SCAN_PASSWORD="scan-password"
python3 scan-history/tenable_io_scan.py                            # edit target_ip first
```

## Limitations / notes

- **These are prototypes.** There is no packaging, no tests, and no configuration file. Targets, ports, credentials, hostnames, and file names are set inside the scripts. The finished version of this work is [NVSRCO](https://github.com/joserico00/NVSRCO).
- **Results are not included.** CSV files, the SQLite database, `.nessus` exports, and OpenVAS reports are generated at runtime and were intentionally left out of the repository.
- **Broken or incomplete files:**
  - `treemap_draft_v2_copy.py` doesn't parse.
  - `treemap_draft_v1.py` and `tabbed_layout_draft.py` fail at startup or in their callbacks.
  - `openvas_scan_skeleton.py` is a stub.
  - The report step in `get_reports.py` fails as written.
  - The string-vs-list `hosts` issue affects `openvas_create_target.py` and `create_target_debug.py`.
  - `tenable_io_scan.py` is untested.
- **Near-duplicates:**
  - There are three identical copies of `network_discovery.py`, and the `vulscan-pipeline/` version is slightly improved.
  - `port_scanner.py` exists in four versions: `-T5` in two copies, and `-T4 -A` in `local-cve-search/` and `vulscan-pipeline/`.
  - `cve_lookup_by_product.py` ≈ `cve_lookup_by_product_quiet.py`, `treemap_draft_v2.py` ≈ `treemap_draft_v2_copy.py`, and `openvas_create_target.py` ≈ `create_target_debug.py`.
  - `nmap_scan_history.py` = `nmap_scan_to_csv.py` + timestamps + append mode.
- **OS and host metadata columns:** the scanners read a host-level `osclass` key (and `nmap_host_details_to_csv.py` also reads `host_distance`, `tcpsequence`, and similar keys). Current python-nmap releases nest OS classes under `osmatch` and don't expose those other keys, so the `OS Details` and related columns usually come out empty or `N/A`.
- **Scope and speed:** subnet-wide `-p-` and `-A` scans of every attached interface can take hours on larger networks, and `-T5` can miss ports on slow links. Appended CSVs are never deduplicated, so they grow across runs and later stages rescan duplicate rows.
- **CVE lookups:** nmap's product and version strings are passed straight to the CVE-Search and NVD endpoints without being normalized to CPE names, so matches are unreliable. `nvd_feed_to_csv.py` relies on a legacy NVD JSON 1.1 feed.
- **Security of the lab setup:** the OpenVAS container and GMP scripts use default admin credentials, CVE-Search requests disable TLS verification, and the Dash apps run with `debug=True`. That is fine on an isolated lab machine, but change it before exposing any of these services.

## Author

Jose E. Rodriguez Rios
