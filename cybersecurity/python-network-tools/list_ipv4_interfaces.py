import socket
import ipaddress
import psutil


def get_ipv4_interfaces():
    ipv4_interfaces = []

    for name, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ipv4_interfaces.append((name, addr.address, addr.netmask))

    return ipv4_interfaces

def main():
    print("working")
    ipv4_interfaces = get_ipv4_interfaces()

    if not ipv4_interfaces:
        print("No active IPv4 network interfaces found.")
    else:
        print("IPv4 network interfaces:")
        for name, ip, netmask in ipv4_interfaces:
            network = ipaddress.IPv4Network((ip, netmask), strict=False)
            print(f"{name}: IP: {ip}, Network: {network}")

if __name__ == "__main__":
    main()