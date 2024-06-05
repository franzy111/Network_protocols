import socket
from argparse import ArgumentParser


def scan_ports(addr, bottom, top):
    try:
        addr = socket.gethostbyname(addr)
    except socket.gaierror as e:
        print(f"Error resolving address: {e}")
        return

    for port in range(bottom, top + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex((addr, port))
            if result == 0:
                print(f"Port {port} is open")
        except socket.error as e:
            print(f"Error scanning port {port}: {e}")
        finally:
            sock.close()


if __name__ == "__main__":
    parser = ArgumentParser(description="TCP port scanner")
    parser.add_argument('--addr', type=str, help='IP address or domain name', default='localhost')
    parser.add_argument('--bottom', type=int, help='Lower bound of port range', default=1)
    parser.add_argument('--top', type=int, help='Upper bound of port range', default=65535)

    args = parser.parse_args()
    scan_ports(args.addr, args.bottom, args.top)
