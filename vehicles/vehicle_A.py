import socket
import ssl


def start_tls_client():

    context = ssl.create_default_context()

    # disable verification for localhost testing
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection(("localhost", 8443)) as sock:

        with context.wrap_socket(sock, server_hostname="localhost") as tls_sock:

            print("Vehicle A connected securely")

            message = input("Enter platoon command: ")
            tls_sock.send(message.encode())

            response = tls_sock.recv(1024)

            print("Vehicle A received:", response.decode())