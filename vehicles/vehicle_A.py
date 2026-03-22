from network.udp_channel import create_udp_socket, send_data, receive_data
from crypto.kyber_exchange import KyberKeyExchange
from crypto.aes_gcm import AESGCMCipher

SERVER_HOST = "localhost"
SERVER_PORT = 8443
SERVER_ADDR = (SERVER_HOST, SERVER_PORT)


def start_udp_client():
    """
    Vehicle A (Leader) - UDP Client

    Protocol:
    1. Send HELLO to Vehicle B (Follower)
    2. Receive Kyber public key from Vehicle B
    3. Encapsulate public key to get ciphertext + shared secret
    4. Send ciphertext to Vehicle B
    5. Encrypt platoon commands with AES-GCM using the shared secret
    """

    kyber = KyberKeyExchange()
    sock = create_udp_socket()

    print("\n[Vehicle A] Leader initiating connection to Follower...\n")

    # === Step 1: Send HELLO ===
    send_data(sock, b"HELLO", SERVER_ADDR)
    print("[Vehicle A] Sent HELLO to Follower")

    # === Step 2: Receive Kyber public key ===
    public_key, _ = receive_data(sock)
    print(f"[Vehicle A] Received Follower's public key ({len(public_key)} bytes)")

    # === Step 3: Encapsulate to get ciphertext + shared secret ===
    print("[Vehicle A] Encapsulating with ML-KEM-768...")
    ciphertext, shared_secret = kyber.encapsulate(public_key)
    print(f"[Vehicle A] Ciphertext size: {len(ciphertext)} bytes")
    print(f"[Vehicle A] Shared secret derived ({len(shared_secret)} bytes)")

    # === Step 4: Send ciphertext to Vehicle B ===
    send_data(sock, ciphertext, SERVER_ADDR)
    print("[Vehicle A] Sent ciphertext to Follower")
    print("[Vehicle A] Post-Quantum key exchange complete!\n")

    # === Step 5: Encrypt and send platoon commands ===
    cipher = AESGCMCipher(shared_secret)

    print("=" * 50)
    print("  Secure Platoon Command Channel Established")
    print("  Type 'exit' to end the session")
    print("=" * 50)

    while True:
        command = input("\n[Vehicle A] Enter platoon command: ")

        if command.lower() == "exit":
            send_data(sock, b"EXIT", SERVER_ADDR)
            print("[Vehicle A] Session ended.")
            break

        nonce, encrypted_command = cipher.encrypt(command.encode())

        # Send nonce + ciphertext together
        send_data(sock, nonce + encrypted_command, SERVER_ADDR)
        print(f"[Vehicle A] Sent encrypted command ({len(nonce) + len(encrypted_command)} bytes)")

    sock.close()
    print("[Vehicle A] Connection closed.")


if __name__ == "__main__":
    start_udp_client()