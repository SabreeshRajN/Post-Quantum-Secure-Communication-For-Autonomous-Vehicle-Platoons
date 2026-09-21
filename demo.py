"""Interactive security demos for the post-quantum platoon.

    python demo.py handshake      # show key transfer + secure session setup
    python demo.py mitm           # man-in-the-middle: blocked when auth is ON
    python demo.py mitm off       # ...and what happens when auth is OFF
    python demo.py replay         # replayed packet is rejected (and off = accepted)
    python demo.py tamper         # a flipped byte is caught by AES-GCM
    python demo.py firmware       # forged OTA firmware is refused
    python demo.py all            # run every scenario
"""

import sys
import threading
import time

from cryptography.exceptions import InvalidTag

from identity.pki import provision_platoon
from protocol.session import ReplayError
from protocol.handshake import follower_handshake
from crypto.dilithium_sign import SignatureError
from network.udp_channel import UdpChannel
from vehicles.vehicle import run_follower, connect_to_followers, send_command, disconnect
from ota.ota_server import OtaServer
from ota.updater import install_update, UpdateRejected
from attacks.mitm import run_mitm
from utils import console

HOST = "127.0.0.1"


# --------------------------------------------------------------------------- #
# 1. Handshake: key transfer + secure session setup
# --------------------------------------------------------------------------- #
def scenario_handshake():
    console.title("SCENARIO 1: Authenticated key exchange & session setup")
    ca_public, creds = provision_platoon(["leader", "follower-1"])
    addr = (HOST, 9201)

    threading.Thread(
        target=run_follower, args=(addr, creds["follower-1"], ca_public),
        kwargs={"log": lambda m: console.step(m)}, daemon=True,
    ).start()
    time.sleep(0.3)

    print(console.bold("\nLeader connects and performs the authenticated handshake:"))
    links = connect_to_followers([("follower-1", addr)], creds["leader"], ca_public,
                                 log=lambda m: console.step(m))
    console.ok("secure session established -- both sides hold the same AES key")

    print(console.bold("\nNow send an encrypted command over the session:"))
    send_command(links, "SET GAP 20m", log=lambda m: console.step(m))
    disconnect(links)


# --------------------------------------------------------------------------- #
# 2. Man-in-the-middle
# --------------------------------------------------------------------------- #
def _safe_follower(addr, cred, ca_public, secure):
    try:
        run_follower(addr, cred, ca_public, secure=secure, log=lambda m: None)
    except SignatureError:
        pass  # in secure mode the follower also rejects the attacker; expected


def scenario_mitm(secure=True, base_port=9210):
    mode = "ON" if secure else "OFF"
    console.title(f"SCENARIO 2: Man-in-the-middle attack (identity checks {mode})")
    ca_public, creds = provision_platoon(["leader", "follower-1"])
    attacker_addr = (HOST, base_port)      # the leader is (mis)pointed here
    follower_addr = (HOST, base_port + 1)

    threading.Thread(target=_safe_follower,
                     args=(follower_addr, creds["follower-1"], ca_public, secure),
                     daemon=True).start()
    time.sleep(0.3)
    threading.Thread(target=run_mitm,
                     args=(attacker_addr, follower_addr, lambda m: console.danger(m)),
                     daemon=True).start()
    time.sleep(0.3)

    print(console.bold("Leader tries to reach follower-1 -- but the address is the attacker's:"))
    try:
        links = connect_to_followers([("follower-1", attacker_addr)],
                                     creds["leader"], ca_public, secure=secure,
                                     log=lambda m: console.step(m))
    except SignatureError:
        console.blocked("MITM stopped: attacker's certificate is not signed by the trusted CA.")
        console.blocked("The leader refuses to establish a session. Attack failed.")
        return

    # secure=False path: the attack succeeds and we see it steal/modify traffic.
    console.danger("handshake completed THROUGH the attacker (no identity checks)")
    print(console.bold("\nLeader sends commands; watch the attacker read and change them:"))
    send_command(links, "SET GAP 20m", log=lambda m: console.step(m))
    send_command(links, "SET GAP 25m", log=lambda m: console.step(m))
    disconnect(links)
    time.sleep(0.2)
    console.danger("Without authentication, the attacker read every command and injected a fake BRAKE.")


# --------------------------------------------------------------------------- #
# 3. Replay  4. Tamper  (shown at the session level: capture a real packet)
# --------------------------------------------------------------------------- #
def _two_sessions(check_replay=True):
    """Build a matched leader/follower session pair without any network."""
    from crypto.kyber_exchange import KyberKeyExchange
    from crypto.hkdf_session import derive_session_key
    from protocol.session import Session
    kem = KyberKeyExchange()
    pk, sk = kem.generate_keypair()
    ct, ss1 = kem.encapsulate(pk)
    ss2 = kem.decapsulate(sk, ct)
    key = derive_session_key(ss1)
    assert key == derive_session_key(ss2)
    return Session(key), Session(key, check_replay=check_replay)


def scenario_replay(secure=True):
    mode = "ON" if secure else "OFF"
    console.title(f"SCENARIO 3: Replay attack (replay protection {mode})")
    leader, follower = _two_sessions(check_replay=secure)

    packet = leader.encrypt(b"OPEN GATE")
    console.step("attacker captures this encrypted packet off the air")
    payload, seq, _ = follower.decrypt(packet)
    console.step(f'follower accepts genuine command: "{payload.decode()}" (seq {seq})')

    console.step("attacker re-sends the SAME captured packet...")
    try:
        payload, seq, _ = follower.decrypt(packet)
        console.danger(f'follower acted on the command AGAIN: "{payload.decode()}" (replay succeeded)')
    except ReplayError as e:
        console.blocked(f"replay rejected -- {e}")


def scenario_tamper():
    console.title("SCENARIO 4: Message tampering (AES-GCM integrity)")
    leader, follower = _two_sessions()

    packet = bytearray(leader.encrypt(b"SET SPEED 30"))
    console.step("genuine command 'SET SPEED 30' sent, encrypted")
    packet[25] ^= 0x01  # flip one bit somewhere in the ciphertext
    console.step("attacker flips a single bit in the ciphertext in transit")
    try:
        follower.decrypt(bytes(packet))
        console.danger("tampered packet accepted!")
    except InvalidTag:
        console.blocked("tampering caught -- AES-GCM auth tag fails, packet discarded")


# --------------------------------------------------------------------------- #
# 5. Forged firmware (OTA)
# --------------------------------------------------------------------------- #
def scenario_firmware():
    console.title("SCENARIO 5: Forged OTA firmware update")
    ota = OtaServer()

    good = ota.publish("v1.2.0", b"\x00safe-brake-controller-image")
    console.step("manufacturer publishes firmware v1.2.0, signed with Dilithium")
    console.ok(install_update(good, ota.public_key))

    print()
    console.step("attacker crafts malicious firmware and fakes a signature")
    forged = ota.publish("v1.2.0", b"\x00safe-brake-controller-image")
    forged.image = b"\x00MALICIOUS-firmware-image"  # changed AFTER signing
    try:
        install_update(forged, ota.public_key)
        console.danger("malicious firmware installed!")
    except UpdateRejected as e:
        console.blocked(f"update refused -- {e}")


SCENARIOS = {
    "handshake": lambda: scenario_handshake(),
    "mitm": None,       # takes on/off
    "mitm_off": None,
    "replay": None,     # takes on/off
    "tamper": lambda: scenario_tamper(),
    "firmware": lambda: scenario_firmware(),
}


def main():
    args = sys.argv[1:]
    name = args[0] if args else "all"
    toggle = (len(args) > 1 and args[1].lower() == "off")
    secure = not toggle

    if name == "handshake":
        scenario_handshake()
    elif name == "mitm":
        scenario_mitm(secure)
    elif name == "replay":
        scenario_replay(secure)
    elif name == "tamper":
        scenario_tamper()
    elif name == "firmware":
        scenario_firmware()
    elif name == "all":
        scenario_handshake()
        scenario_mitm(secure=True, base_port=9210)
        scenario_mitm(secure=False, base_port=9220)
        scenario_replay(secure=True)
        scenario_tamper()
        scenario_firmware()
    else:
        print(__doc__)
        return
    print()


if __name__ == "__main__":
    main()
