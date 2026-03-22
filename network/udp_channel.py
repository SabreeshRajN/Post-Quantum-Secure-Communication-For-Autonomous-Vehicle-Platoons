import socket

# Default settings for local simulation
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8443
BUFFER_SIZE = 4096


def create_udp_socket():
    """Create a standard UDP socket."""
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def bind_socket(sock, host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Bind a UDP socket to the given host and port."""
    sock.bind((host, port))
    print(f"[UDP] Socket bound to {host}:{port}")


def send_data(sock, data, address):
    """Send raw bytes over UDP to the specified address."""
    sock.sendto(data, address)


def receive_data(sock, buffer_size=BUFFER_SIZE):
    """Receive raw bytes from a UDP socket. Returns (data, address)."""
    data, address = sock.recvfrom(buffer_size)
    return data, address
