from network.udp_channel import create_udp_socket, bind_socket, send_data, receive_data
from crypto.kyber_exchange import KyberKeyExchange
from crypto.aes_gcm import AESGCMCipher

SERVER_HOST = "localhost"
SERVER_PORT = 8443


def start_udp_server():
    """
    Vehicle B (Follower) - UDP Server

    Protocol:
    1. Wait for HELLO from Vehicle A (Leader)
    2. Generate Kyber keypair and send public key
    3. Receive ciphertext, decapsulate to get shared secret
    4. Receive AES-GCM encrypted commands using the shared secret
    """

    kyber = KyberKeyExchange()
    sock = create_udp_socket()
    bind_socket(sock, SERVER_HOST, SERVER_PORT)

    print("\n[Vehicle B] Follower waiting for Leader connection...\n")

    # === Step 1: Wait for HELLO from Vehicle A ===
    data, client_addr = receive_data(sock)
    print(f"[Vehicle B] Received '{data.decode()}' from Leader at {client_addr}")

    # === Step 2: Generate Kyber keypair and send public key ===
    print("[Vehicle B] Generating ML-KEM-768 keypair...")
    public_key, secret_key = kyber.generate_keypair()
    print(f"[Vehicle B] Public key size: {len(public_key)} bytes")
    print(f"[Vehicle B] Secret key size: {len(secret_key)} bytes")

    send_data(sock, public_key, client_addr)
    print("[Vehicle B] Sent public key to Leader\n")

    # === Step 3: Receive ciphertext and decapsulate ===
    ciphertext, _ = receive_data(sock)
    print(f"[Vehicle B] Received ciphertext ({len(ciphertext)} bytes)")

    shared_secret = kyber.decapsulate(secret_key, ciphertext)
    print(f"[Vehicle B] Shared secret derived ({len(shared_secret)} bytes)")
    print("[Vehicle B] Post-Quantum key exchange complete!\n")

    # === Step 4: Receive and decrypt AES-GCM encrypted commands ===
    cipher = AESGCMCipher(shared_secret)

    print("[Vehicle B] Listening for encrypted platoon commands...\n")

    while True:
        encrypted_data, _ = receive_data(sock)

        if encrypted_data == b"EXIT":
            print("[Vehicle B] Leader ended session.")
            break

        # First 12 bytes = nonce, rest = ciphertext
        nonce = encrypted_data[:12]
        ct = encrypted_data[12:]

        plaintext = cipher.decrypt(nonce, ct)
        print(f"[Vehicle B] Decrypted command: {plaintext.decode()}")

    sock.close()
    print("[Vehicle B] Connection closed.")


if __name__ == "__main__":
    start_udp_server()