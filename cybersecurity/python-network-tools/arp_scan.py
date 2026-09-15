import sys
from scapy.all import ARP, Ether, srp
from ipaddress import IPv4Network

def arp_scan(target_subnet):
    # Create an ARP request packet to get information about hosts in the target subnet
    arp = ARP(pdst=target_subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Send the ARP request packet and capture the response
    result = srp(packet, timeout=2, verbose=0)[0]

    # List to store the discovered hosts
    hosts = []

    # Parse the response to extract IP and MAC addresses of the live hosts
    for sent, received in result:
        hosts.append({'ip': received.psrc, 'mac': received.hwsrc})

    return hosts

def main():
    if len(sys.argv) != 2:
        print("Usage: python arp_scan.py <target_subnet>")
        sys.exit(1)

    target_subnet = sys.argv[1]

    try:
        IPv4Network(target_subnet)
    except ValueError:
        print("Invalid subnet")
        sys.exit(1)

    print(f"Scanning subnet {target_subnet}...")
    hosts = arp_scan(target_subnet)

    print("Hosts discovered:")
    print("IP Address\t\tMAC Address")
    print("-----------------------------------------")
    for host in hosts:
        print(f"{host['ip']}\t\t{host['mac']}")

if __name__ == "__main__":
    main()