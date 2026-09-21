"""Leader <-> follower secure link over UDP."""

import socket
import time
from network.udp_channel import UdpChannel
from protocol.handshake import leader_handshake, follower_handshake
import utils.telemetry as telemetry
from crypto.dilithium_sign import SignatureError

BUFFER_SIZE = 65536
SOCKET_TIMEOUT = 5.0

class Link:
    def __init__(self, name, addr, sock, session):
        self.name = name
        self.addr = addr
        self.sock = sock
        self.session = session
        self.channel = UdpChannel(sock, addr)

    def send_command(self, command: str, log=lambda m: None):
        packet = self.session.encrypt(command.encode())
        start = time.perf_counter()
        self.channel.send(packet)
        
        data = self.channel.recv(BUFFER_SIZE)
        rtt_ms = (time.perf_counter() - start) * 1000
        ack_payload, _, _ = self.session.decrypt(data)
        
        return rtt_ms, ack_payload.decode()

    def close(self):
        try:
            self.channel.send(self.session.encrypt(b"BYE"))
        except OSError:
            pass
        self.sock.close()

def run_follower(addr, cred, ca_public, secure=True, log=lambda m: None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(addr)
    
    data, leader_addr = sock.recvfrom(BUFFER_SIZE)
    class FirstPacketChannel:
        def __init__(self, sock, addr, first_data):
            self.sock = sock
            self.addr = addr
            self.first_data = first_data
        def send(self, d):
            self.sock.sendto(d, self.addr)
        def recv(self, bufsize=BUFFER_SIZE):
            if self.first_data:
                d = self.first_data
                self.first_data = None
                return d
            d, _ = self.sock.recvfrom(bufsize)
            return d

    channel = FirstPacketChannel(sock, leader_addr, data)
    session = follower_handshake(channel, cred, ca_public, secure=secure, log=log)
    
    while True:
        data, _ = sock.recvfrom(BUFFER_SIZE)
        try:
            payload, seq, _ = session.decrypt(data)
        except Exception:
            continue
            
        command = payload.decode()
        if command == "BYE":
            break
            
        ack_text = f"ACK '{command}' by {cred.vehicle_id}"
        ack_packet = session.encrypt(ack_text.encode())
        sock.sendto(ack_packet, leader_addr)
        
    sock.close()

def connect_to_followers(followers, leader_cred, ca_public, secure=True, log=lambda m: None, timeout=SOCKET_TIMEOUT):
    links = []
    for name, addr in followers:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        channel = UdpChannel(sock, addr)
        try:
            session = leader_handshake(channel, leader_cred, ca_public, secure=secure, log=log)
            links.append(Link(name, addr, sock, session))
        except SignatureError:
            raise  # Bubble up MITM signature errors so demo.py can catch them
        except Exception as e:
            log(f"Failed to connect to {name}: {e}")
            sock.close()
    return links

def send_command(links, command, log=lambda m: None):
    rtts = []
    for link in links:
        try:
            rtt_ms, ack_text = link.send_command(command, log)
            log(f"[{link.name}] {ack_text}  (RTT {rtt_ms:.2f} ms)")
            rtts.append(rtt_ms)
        except socket.timeout:
            log(f"[{link.name}] timed out")
    return rtts

def disconnect(links):
    for link in links:
        link.close()
