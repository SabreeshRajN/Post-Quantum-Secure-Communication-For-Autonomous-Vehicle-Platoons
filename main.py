import threading
import time

from vehicles.vehicle_B import start_udp_server
from vehicles.vehicle_A import start_udp_client


def run_simulation():

    print("\n=== Starting Post-Quantum Secure V2V Communication (UDP) ===")
    print("=== Kyber-768 Key Exchange + AES-256-GCM Encryption ===\n")

    # Start Vehicle B (Follower/Server) in a background thread
    server_thread = threading.Thread(target=start_udp_server, daemon=True)
    server_thread.start()

    # Brief delay to ensure server is listening before client connects
    time.sleep(1)

    # Start Vehicle A (Leader/Client) in main thread (handles user input)
    start_udp_client()

    # Wait for server thread to finish
    server_thread.join(timeout=5)
    print("\n=== Simulation Complete ===")


if __name__ == "__main__":
    run_simulation()