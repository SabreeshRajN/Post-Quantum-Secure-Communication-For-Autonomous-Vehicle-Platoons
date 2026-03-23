import socket
from crypto.kyber_exchange import KyberKeyExchange
from crypto.aes_gcm import AESGCMCipher

HOST = "localhost"
PORT = 8443
BUFFER_SIZE = 4096


def start_udp_client():
    """
    Vehicle A - Leader/Client
    UDP Post-Quantum Key Exchange + AES-GCM secure messaging flow:
      1. Send HELLO to Vehicle B (Follower) to initiate handshake
      2. Receive Vehicle B's Kyber Public Key
      3. Encapsulate -> get shared_secret + ciphertext; send ciphertext to Vehicle B
      4. Use shared_secret as AES-256-GCM key to encrypt and send platoon commands
    """

    kyber = KyberKeyExchange()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (HOST, PORT)

    print("[Vehicle A] Initiating Post-Quantum Key Exchange over UDP...")

    # Step 1: Send HELLO to Vehicle B
    sock.sendto(b"HELLO", server_addr)
    print("[Vehicle A] HELLO sent to Vehicle B.")

    # Step 2: Receive Vehicle B's Kyber Public Key
    public_key, _ = sock.recvfrom(BUFFER_SIZE)
    print(f"[Vehicle A] Received Kyber public key from Vehicle B. Size: {len(public_key)} bytes")

    # Step 3: Encapsulate -> derive shared secret + ciphertext
    ciphertext, shared_secret = kyber.encapsulate(public_key)
    sock.sendto(ciphertext, server_addr)
    print(f"[Vehicle A] Ciphertext sent to Vehicle B. Size: {len(ciphertext)} bytes")
    print(f"[Vehicle A] Shared secret established. Key: {shared_secret.hex()}")

    # Initialize AES-GCM cipher with the shared secret
    cipher = AESGCMCipher(shared_secret)

    print("\n[Vehicle A] Secure channel ready. You can now send platoon commands to the Follower.\n")

    # Continuously send encrypted platoon commands
    while True:
        message = input("[Vehicle A] Enter platoon command (or 'exit' to quit): ").strip()
        if message.lower() == "exit":
            sock.sendto(b"EXIT", server_addr)
            print("[Vehicle A] Disconnected from Vehicle B.")
            break

        encrypted = cipher.encrypt(message)
        print(f"[Vehicle A] Encrypted payload ({len(encrypted)} bytes) sent.")
        sock.sendto(encrypted, server_addr)

        # Wait for ACK from Vehicle B
        ack_payload, _ = sock.recvfrom(BUFFER_SIZE)
        ack = cipher.decrypt(ack_payload)
        print(f"[Vehicle A] Received from Vehicle B: '{ack}'\n")

    sock.close()