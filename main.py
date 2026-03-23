import threading
import time

from vehicles.vehicle_B import start_tls_server
from vehicles.vehicle_A import start_tls_client


def run_simulation():

    print("\n=== Starting Secure V2V Communication ===")

    server_thread = threading.Thread(target=start_tls_server)
    server_thread.start()

    time.sleep(2)

    start_tls_client()


if __name__ == "__main__":
    run_simulation()