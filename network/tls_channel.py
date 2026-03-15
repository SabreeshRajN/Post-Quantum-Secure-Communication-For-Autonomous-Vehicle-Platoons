import socket
import ssl


def start_tls_server():

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 8443))
    server_socket.listen(5)

    print("Vehicle B TLS server listening on port 8443...")

    conn, addr = server_socket.accept()

    with context.wrap_socket(conn, server_side=True) as tls_conn:

        print("Secure TLS connection established with", addr)

        data = tls_conn.recv(1024)
        print("Vehicle B received:", data.decode())

        tls_conn.send(b"Message received securely")

    server_socket.close()