import threading
import time

from vehicles.vehicle_B import start_udp_server
from vehicles.vehicle_A import start_udp_client


def run_simulation():

    print("\n" + "=" * 60)
    print("  Post-Quantum Secure V2V Platoon Communication")
    print("  Protocol: ML-KEM-768 (Kyber) + AES-256-GCM over UDP")
    print("=" * 60)

    # Start Vehicle B (Follower/Server) in a background thread
    server_thread = threading.Thread(target=start_udp_server, daemon=True)
    server_thread.start()

    # Give the server time to bind
    time.sleep(1)

    # Start Vehicle A (Leader/Client) in the main thread
    start_udp_client()


if __name__ == "__main__":
    run_simulation()