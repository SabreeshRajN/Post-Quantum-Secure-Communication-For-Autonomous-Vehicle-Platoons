"""Run the post-quantum secure platoon: 1 leader + N followers, interactive.

    python main.py            # 2 followers (default)
    python main.py 3          # 3 followers
"""

import sys
import threading
import time

from identity.pki import provision_platoon
from vehicles.vehicle import (
    run_follower, connect_to_followers, send_command, disconnect,
)
import utils.telemetry as telemetry

HOST = "127.0.0.1"
BASE_PORT = 8443


def main():
    num_followers = int(sys.argv[1]) if len(sys.argv) > 1 else 2

    print("\n=== Post-Quantum Secure V2V Platoon ===")
    print("=== Kyber-768 KEM + Dilithium auth + AES-256-GCM ===\n")

    # Factory step: hand every vehicle an identity + CA-signed certificate.
    vehicle_ids = ["leader"] + [f"follower-{i}" for i in range(1, num_followers + 1)]
    ca_public, creds = provision_platoon(vehicle_ids)
    print(f"[PKI] issued identities to {num_followers} follower(s) + leader\n")

    # Start each follower as a UDP server in its own thread (quiet: see demo.py
    # for the full step-by-step handshake narration).
    quiet = lambda m: None
    followers = []
    for i in range(1, num_followers + 1):
        name = f"follower-{i}"
        addr = (HOST, BASE_PORT + i)
        threading.Thread(
            target=run_follower, args=(addr, creds[name], ca_public),
            kwargs={"log": quiet}, daemon=True,
        ).start()
        followers.append((name, addr))

    time.sleep(0.5)  # let followers bind before the leader connects

    # Leader runs the authenticated handshake with each follower.
    links = connect_to_followers(followers, creds["leader"], ca_public, log=quiet)
    for link in links:
        print(f"[leader] authenticated + secure session with {link.name}")
    print("\n[leader] all secure sessions ready. Type platoon commands.\n")

    while True:
        command = input("[leader] command (or 'exit'): ").strip()
        if command.lower() == "exit":
            disconnect(links)
            break
        if not command:
            continue
        rtts = send_command(links, command)
        for rtt in rtts:
            telemetry.record_rtt(rtt)

    print("\n[System] rendering benchmark dashboard...")
    telemetry.show_dashboard()
    print("=== platoon stopped ===")


if __name__ == "__main__":
    main()
