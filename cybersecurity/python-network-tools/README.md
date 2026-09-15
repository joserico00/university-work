# Python Network Tools

A collection of small Python networking scripts written while learning how host discovery, port scanning, and packet capture work at a low level. They cover working out which subnet the machine is on, host discovery with ARP, ICMP, and TCP connects, SYN port scanning with Scapy, automating nmap through `python-nmap` and `python3-nmap`, simple CVE lookups against the NVD, and a traffic graph built from sniffed packets. Most files are short experiments rather than finished tools, and the incomplete ones are marked below. The subnet-scanner pattern in `nmap_port_scan.py` / `nmap_syn_scan_to_file.py` (find interfaces with `psutil`, then scan with `python-nmap`) was carried forward into the later `network-scanner-prototypes` repository and eventually the [NVSRCO](https://github.com/joserico00/NVSRCO) graduate project.

> **Legal / ethical use.** These scripts send ARP, ICMP, and TCP probes, run nmap scans, and capture traffic. Only use them on networks you own or have explicit written permission to test. Scanning or sniffing other networks may be illegal and may break acceptable-use policies.

## How it works

The scripts line up with the usual reconnaissance steps:

```
1. Local network info     local_network_info.py, interface_netmask.py, list_ipv4_interfaces.py, route_source_ip.py
   "which subnet am I on?"
          |
          v
2. Host discovery         arp_scan_basic.py, arp_scan_local.py, arp_scan.py    ARP        (Scapy)
                          icmp_ping.py                                        ICMP echo  (Scapy)
                          tcp_ping_sweep.py                                 TCP connect to :80
          |
          v
3. Port scanning          syn_port_scan.py, ping_and_syn_scan.py, tcp_syn_scan_stub.py    TCP SYN    (Scapy)
                          nmap_port_scan.py, nmap_syn_scan_to_file.py, python_nmap_examples.py,          nmap
                          nmap3_examples.py
          |
          v
4. Vulnerability lookup   nmap_nvd_api_lookup.py, nmap_nvd_web_lookup.py                       nmap + NVD

5. Traffic / review       traffic_graph.py   sniff -> directed graph
                          scan_results_analysis.ipynb     review your own scanner CSV output with pandas
```

The scripts use two different approaches:

- **Hand-built packets with Scapy.** ARP discovery sends `Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=<range>)` as a broadcast with `srp()` and reads each reply's `psrc` (IP) and `hwsrc` (MAC). Ping sends `IP(dst=...) / ICMP()` with `sr1()`. The SYN scan sends `IP(dst=...) / TCP(dport=p, flags="S")`: a reply with TCP flags `0x12` (SYN-ACK) means the port is open, and a RST is then sent to close the half-open connection. All of these use raw sockets, so they need root.
- **nmap through python-nmap.** `psutil.net_if_addrs()` lists each interface's IPv4 address and netmask. `ipaddress.IPv4Network((ip, netmask), strict=False)` turns that pair into the subnet, and loopback `127.0.0.0/8` is skipped. The subnet goes to `nmap.PortScanner().scan(hosts=..., arguments=...)`, and the result dict is walked host → protocol → port.

## Files

### Local network information

| File | What it does | Inputs | Outputs |
|---|---|---|---|
| `local_network_info.py` | **Experiment.** Gets the machine's IP with `socket.gethostbyname(socket.gethostname())` and builds `ipaddress.ip_network(IP)`. It prints the network with prefix, hostmask, and netmask forms, and its type, then prints `cidrize(IP)`. No netmask is supplied, so the "network" is always a single-address `/32` and the real subnet is never shown. It imports `pyroute2.IPRoute` for an interface listing that is commented out, but the import is still executed. | none | console |
| `interface_netmask.py` | Uses `netifaces` to print all interface names and the address info for the hardcoded interface `en0` (the macOS default). It then works out the prefix length from that interface's broadcast address and netmask with `ipaddress.IPv4Network(..., strict=False)`. | none (`en0` hardcoded) | console |
| `list_ipv4_interfaces.py` | Standalone version of the `get_ipv4_interfaces()` helper later used by the nmap scanners. It walks `psutil.net_if_addrs()`, keeps `AF_INET` addresses, and prints `name: IP: <ip>, Network: <subnet>` for every interface, loopback included. | none | console |
| `route_source_ip.py` | Third-party snippet (Apache-2.0 header, copyright IBM, kept as-is) that returns the local interface IP used to route to a given host. It resolves the host with `netaddr`/`socket`, asks the kernel with pyroute2 `IPRoute().route("get", dst=...)`, and reads a fixed position in the route attributes. **Does not run standalone:** it imports `lib.logger`, a module from its original project that isn't in this project. The netlink route lookup is Linux-specific. | positional `host` (argparse) | console |

### Host discovery

| File | What it does | Inputs | Outputs |
|---|---|---|---|
| `arp_scan_basic.py` | `arp_scan(ip)` broadcasts an ARP request for a range, calls `srp(timeout=3, retry=2)`, and returns a list of `{"IP": ..., "MAC": ...}` dicts. The call at the bottom of the file scans a hardcoded `/24`, so edit it before running. The trailing comments (in Spanish) are notes on next steps: ping each machine, collect hardware addresses. | hardcoded range | one dict per host on the console |
| `arp_scan_local.py` | ARP scan of the machine's own IP with a hardcoded `/19` appended as the range (`srp` timeout 1 s). Prints `IP  MAC` for each reply. An `ip_network` object is computed but never used. | none | console |
| `arp_scan.py` | The most complete ARP scanner in the repo. It takes one argument, validates it with `IPv4Network()` (strict, so it must be a network address such as `192.168.1.0/24`), scans with `srp(timeout=2, verbose=0)`, and prints an IP/MAC table. The usage message refers to it as `arp_scan.py`. | `sys.argv[1]` = subnet | table on the console |
| `icmp_ping.py` | Sends one ICMP echo request with `sr1(timeout=10)` and prints `online` or `ofline` (sic). | `sys.argv[1]` = IP | console |
| `tcp_ping_sweep.py` | TCP-connect sweep that doesn't need Scapy or root. For `.1` to `.255` of a hardcoded `/24` prefix (the `subnet` variable), it tries to connect to port 80 with a 1-second timeout and prints `<ip> is up!` on success. It only finds hosts listening on port 80. The `socket.close()` call runs on the module instead of the socket object, so it raises, and the bare `except` swallows the error. | hardcoded prefix | console |

### Port scanning with Scapy

| File | What it does | Inputs | Outputs |
|---|---|---|---|
| `syn_port_scan.py` | SYN-scans the machine's own IP (resolved from the hostname) over `range(1, 10)`, which is ports 1–9. The `sys.argv` parsing is commented out. For each port it sends a SYN and checks for SYN-ACK (`0x12`), then sends a RST. **Two bugs:** if a port doesn't reply, `response` is `None` and `.haslayer()` raises `AttributeError`. Also, `'Port '+str(port)+' 'is open` is parsed as an identity comparison with the built-in `open`, so it prints `False` instead of a message. | `firstport` / `lastport` variables | console |
| `ping_and_syn_scan.py` | The code from `icmp_ping.py` and `syn_port_scan.py` wrapped as `ping(ip)` and `portsniffer(adress, firstport, lastport)`. **Nothing is called at module level**, so running the file does nothing. If `portsniffer()` is called, it fails on the undefined name `endport` and has the same `None`/print problems as `syn_port_scan.py`. | function arguments | console |
| `tcp_syn_scan_stub.py` | **Stub.** `tcp_scan(ip, ports)` builds a SYN packet inside a `try` block. The field `dst` is misspelled `dsp`, the `except` only constructs a `socket.gaierror` without raising it, and the packet is never sent. No output. | hardcoded ports `[1, 100]` | none |
| `scapy_stub.py` | **Placeholder.** Contains only `from scapy import *`. | – | – |

### Port scanning with nmap

| File | What it does | Inputs | Outputs |
|---|---|---|---|
| `nmap_port_scan.py` | For each non-loopback interface subnet, runs `nm.scan(hosts=<subnet>, arguments="-p <start>-<end>")` and prints each host with its hostname and each protocol with the sorted list of ports nmap reported. The port list isn't filtered by state. | `<start_port> <end_port>` | console |
| `nmap_syn_scan_to_file.py` | Same arguments and loop as `nmap_port_scan.py`, but the scan uses `-p <start>-<end> -sS --host-timeout 10m` (a SYN scan, so it needs root). Results go to `scan_results.txt` instead of the console. For each host it writes hostnames, MAC address, "OS Details", and **open ports only** per protocol. OS details are usually `N/A`: no `-O` flag is passed, and the code reads a host-level `osclass` key that current python-nmap nests under `osmatch`. | `<start_port> <end_port>` | `scan_results.txt` (overwritten), subnet printed to console |
| `python_nmap_examples.py` | Exploration of the python-nmap API against a hardcoded IP. It scans ports 22–443 and prints hostname, state, protocols, and TCP port keys. Next it ping-sweeps that IP's `/24` (`-n -sP -PE -PA21,23,80,3389`) and prints `(host, status)` pairs. Finally it runs a default nmap scan (top 1000 ports) on each discovered host and prints every port's state along with the raw port dicts. | hardcoded `ip` | console |
| `nmap3_examples.py` | Tour of the `python3-nmap` (`nmap3`) API against a hardcoded IP, which overrides the hostname lookup. It runs OS detection (twice), top-ports scan, list scan, subnet scan, TCP scan, ping scan, and ARP discovery (twice), printing each raw result. The last two sections print the ping-scan `result` variable instead of the ARP `results`. It also imports Scapy and builds an ARP packet that is never used. OS detection needs root. | hardcoded `IPAddr` | console |

### Vulnerability lookup

| File | What it does | Inputs | Outputs |
|---|---|---|---|
| `nmap_nvd_api_lookup.py` | Scans a hardcoded `/24` target on ports 1–1024 (python-nmap's default arguments include `-sV`). It collects the unique TCP service names and, for each one, queries the NVD REST API **1.0** with `cpeMatchString=cpe:2.3:a:*:<service>:*...`, then prints the CVE IDs. **As written it exits early:** the check `target_ip not in scanner.all_hosts()` compares the CIDR string to individual host IPs, never matches, and prints "Failed to scan". Even past that check, the 1.0 API has been retired, and service names such as `http` aren't CPE product names. | hardcoded `target_ip`, `target_ports` | console |
| `nmap_nvd_web_lookup.py` | For each non-loopback subnet it runs `-p <start>-<end> -sS -O --host-timeout 10m`, which needs root. For every port found, `check_vulnerabilities(service, version)` requests the NVD website's search results page (`nvd.nist.gov/vuln/search/results`) with `query="<service> <version>"` and scrapes the CVE link text from `span.col-md-2` elements with BeautifulSoup. It writes one `Service, Version, Vulnerabilities` line per port. This makes one HTTP request per port, with no rate limiting, and the scraping depends on NVD's page markup. | `<start_port> <end_port>` | `scan_results.txt` (overwritten) |

### Traffic analysis and data review

| File | What it does | Inputs | Outputs |
|---|---|---|---|
| `traffic_graph.py` | Calls `sniff(prn=process_packet, filter="ip", timeout=60)` on the default interface and records a `(src, dst)` pair for every IP packet. `create_graph()` builds a `networkx.DiGraph` whose edge weight is the packet count. `draw_graph()` lays it out with `spring_layout`, sets edge width from the weight, and shows it with matplotlib. The edge-label dict is keyed by weight values instead of `(src, dst)` pairs, so drawing the edge labels will likely raise a `TypeError` before the window appears. Needs root to sniff. | 60 s of live traffic | matplotlib window |
| `scan_results_analysis.ipynb` | pandas notebook (Python 3.9 kernel) that you run against your own scan CSVs. It loads `oldscan_results.csv` and `scan_results.csv`, displays both, and filters rows where `State == "closed"`. The expected columns (`IP, Hostname, MAC Address, OS Details, Protocol, Port, Name, State, Product, Version, Extra Info, Uptime, ...`) match the CSV written by the nmap scanners in `network-scanner-prototypes`. The notebook is committed with its outputs cleared, so it contains no scan results; the CSV files are not included, and the last cell is empty. | two CSV files in the working directory | notebook output |

## Requirements

- **Python 3.6+.** f-strings are used throughout, and the notebook metadata shows Python 3.9. None of the scripts use Python 2 print statements. `route_source_ip.py` carries `from __future__` imports from its original codebase, but they are harmless on Python 3.
- **Python packages** (inferred from the imports):

  | Package | Used by |
  |---|---|
  | `scapy` | `arp_scan_basic.py`, `arp_scan_local.py`, `arp_scan.py`, `icmp_ping.py`, `syn_port_scan.py`, `ping_and_syn_scan.py`, `tcp_syn_scan_stub.py`, `traffic_graph.py`, `nmap3_examples.py` |
  | `python-nmap` (imported as `nmap`) | `nmap_port_scan.py`, `nmap_syn_scan_to_file.py`, `python_nmap_examples.py`, `nmap_nvd_api_lookup.py`, `nmap_nvd_web_lookup.py` |
  | `python3-nmap` (imported as `nmap3`) | `nmap3_examples.py` |
  | `psutil` | `list_ipv4_interfaces.py`, `nmap_port_scan.py`, `nmap_syn_scan_to_file.py`, `nmap_nvd_web_lookup.py` |
  | `netifaces` | `interface_netmask.py` |
  | `pyroute2`, `cidrize` | `local_network_info.py` |
  | `pyroute2`, `netaddr` | `route_source_ip.py` |
  | `requests` | `nmap_nvd_api_lookup.py`, `nmap_nvd_web_lookup.py` |
  | `beautifulsoup4` | `nmap_nvd_web_lookup.py` |
  | `networkx`, `matplotlib` | `traffic_graph.py` |
  | `pandas`, `numpy`, `jupyter` | `scan_results_analysis.ipynb` |

- **External tools:**
  - The `nmap` binary on `PATH`. Both `python-nmap` and `python3-nmap` are wrappers around it.
  - libpcap for Scapy sniffing with BPF filters. It ships with macOS; on Debian/Ubuntu, install `libpcap-dev`.
- **Root / sudo** is needed for anything that sends raw packets or sniffs: every Scapy script (ARP, ICMP, SYN, `sniff`), and nmap runs that use `-sS` or `-O` (`nmap_syn_scan_to_file.py`, `nmap_nvd_web_lookup.py`, OS detection in `nmap3_examples.py`). `nmap_port_scan.py`, `python_nmap_examples.py`, `nmap_nvd_api_lookup.py`, `tcp_ping_sweep.py`, and the interface-info scripts run without root. Without root, nmap falls back to slower TCP connect scans and less reliable host discovery.
- **Platform notes:** `interface_netmask.py` assumes an interface named `en0` (macOS). `route_source_ip.py` relies on pyroute2's netlink route lookup, which is Linux-specific.

## Usage

```bash
pip install scapy python-nmap python3-nmap psutil netifaces netaddr pyroute2 cidrize \
            requests beautifulsoup4 networkx matplotlib pandas jupyter

# Local network info
python3 list_ipv4_interfaces.py
python3 interface_netmask.py

# Host discovery
sudo python3 arp_scan.py 192.168.1.0/24
sudo python3 icmp_ping.py 192.168.1.10

# nmap-based subnet scanners (scan every subnet this machine is attached to)
python3 nmap_port_scan.py 1 1024                 # results on the console
sudo python3 nmap_syn_scan_to_file.py 1 1024           # -> scan_results.txt
sudo python3 nmap_nvd_web_lookup.py 20 443          # -> scan_results.txt with NVD search hits

# Traffic graph (sniffs for 60 seconds, then opens a plot)
sudo python3 traffic_graph.py

# Route lookup (needs lib/logger.py from its original project)
python3 route_source_ip.py example.com

# Notebook (place your own oldscan_results.csv and scan_results.csv next to it first)
jupyter notebook scan_results_analysis.ipynb
```

These scripts take no arguments, so edit the hardcoded values before running them:

| Script | Variable to edit |
|---|---|
| `arp_scan_basic.py` | the range passed to `arp_scan(...)` at the bottom |
| `arp_scan_local.py` | the `'/19'` suffix |
| `tcp_ping_sweep.py` | `subnet` (first three octets, e.g. `"192.168.1."`) |
| `syn_port_scan.py` | `firstport`, `lastport` (target is always the local machine) |
| `python_nmap_examples.py` | `ip` |
| `nmap3_examples.py` | `IPAddr` (the second assignment) |
| `nmap_nvd_api_lookup.py` | `target_ip`, `target_ports` |

If the packages are installed in a virtual environment, run `sudo "$(which python3)" script.py` so the root process uses the same interpreter.

## Limitations / notes

- These are learning scripts, not maintained tools. Error handling is minimal, several use bare `except:` blocks, and nothing is packaged or tested.
- **Non-working or incomplete files:** `scapy_stub.py` (placeholder), `tcp_syn_scan_stub.py` (stub, sends nothing), `ping_and_syn_scan.py` (functions never called, undefined `endport`), `syn_port_scan.py` (crashes on unanswered ports, prints `False`), `nmap_nvd_api_lookup.py` (always exits before the lookup, and uses a retired NVD API), `route_source_ip.py` (missing `lib.logger`), and the edge labels in `traffic_graph.py`.
- **Near-duplicates:** `nmap_syn_scan_to_file.py` is `nmap_port_scan.py` plus a SYN scan, file output, MAC/OS fields, and an open-port filter. `nmap_nvd_web_lookup.py` is `nmap_syn_scan_to_file.py` plus `-O` and an NVD lookup per port. `ping_and_syn_scan.py` is `icmp_ping.py` and `syn_port_scan.py` combined. `arp_scan_basic.py`, `arp_scan_local.py`, and `arp_scan.py` are three versions of the same ARP scan.
- `socket.gethostbyname(socket.gethostname())`, used in `local_network_info.py`, `arp_scan_local.py`, `syn_port_scan.py`, `tcp_syn_scan_stub.py`, and `nmap3_examples.py`, can return `127.0.0.1` or the address of the wrong interface depending on the hosts file. The `psutil`-based approach in `list_ipv4_interfaces.py` and the scanners is more reliable.
- `nmap_port_scan.py`, `nmap_syn_scan_to_file.py`, and `nmap_nvd_web_lookup.py` scan every subnet the machine is attached to. On a large network (for example a `/16`), this can take a long time and generate a lot of traffic.
- `nmap_syn_scan_to_file.py` and `nmap_nvd_web_lookup.py` both write to `scan_results.txt`, so each run overwrites the other's output.
- Output files (`scan_results.txt`, and the CSVs the notebook reads) are generated at runtime and are not included in the repository. `scan_results_analysis.ipynb` is saved without cell outputs, so run it against your own scan CSVs to see results.

## Author

Jose E. Rodriguez Rios
