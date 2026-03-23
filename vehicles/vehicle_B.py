import socket
from crypto.kyber_exchange import KyberKeyExchange
from crypto.aes_gcm import AESGCMCipher

HOST = "localhost"
PORT = 8443
BUFFER_SIZE = 4096


def start_udp_server():
    """
    Vehicle B - Follower/Server
    UDP Post-Quantum Key Exchange + AES-GCM secure messaging flow:
      1. Wait for HELLO from Vehicle A (Leader)
      2. Generate Kyber keypair, send Public Key to Vehicle A
      3. Receive Ciphertext from Vehicle A, decapsulate -> shared_secret
      4. Use shared_secret as AES-256-GCM key to decrypt incoming messages
    """

    kyber = KyberKeyExchange()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    print(f"[Vehicle B] UDP server listening on {HOST}:{PORT}...")

    # Step 1: Wait for HELLO from Vehicle A
    data, addr = sock.recvfrom(BUFFER_SIZE)
    if data == b"HELLO":
        print(f"[Vehicle B] Received HELLO from Vehicle A at {addr}")
    else:
        print("[Vehicle B] Unexpected initiation message. Aborting.")
        sock.close()
        return

    # Step 2: Generate Kyber-768 keypair and send public key
    public_key, secret_key = kyber.generate_keypair()
    print(f"[Vehicle B] Kyber keypair generated. Public key size: {len(public_key)} bytes")
    sock.sendto(public_key, addr)
    print("[Vehicle B] Public key sent to Vehicle A.")

    # Step 3: Receive ciphertext from Vehicle A
    ciphertext, _ = sock.recvfrom(BUFFER_SIZE)
    print(f"[Vehicle B] Received ciphertext from Vehicle A. Size: {len(ciphertext)} bytes")

    # Step 4: Decapsulate to get shared secret
    shared_secret = kyber.decapsulate(secret_key, ciphertext)
    print(f"[Vehicle B] Shared secret established. Key: {shared_secret.hex()}")

    # Initialize AES-GCM cipher with the shared secret
    cipher = AESGCMCipher(shared_secret)

    print("\n[Vehicle B] Secure channel ready. Awaiting encrypted platoon commands from Leader...\n")

    # Continuously receive and decrypt messages
    while True:
        payload, _ = sock.recvfrom(BUFFER_SIZE)
        if payload == b"EXIT":
            print("[Vehicle B] Leader disconnected. Shutting down.")
            break
        try:
            message = cipher.decrypt(payload)
            print(f"[Vehicle B] Decrypted platoon command: '{message}'")
            response = f"ACK: '{message}' received and applied."
            encrypted_response = cipher.encrypt(response)
            sock.sendto(encrypted_response, addr)
        except Exception as e:
            print(f"[Vehicle B] Decryption failed: {e}")

    sock.close()