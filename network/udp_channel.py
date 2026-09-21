"""Thin send()/recv() wrapper over a UDP socket."""

import socket

class UdpChannel:
    def __init__(self, sock: socket.socket, addr: tuple):
        self._sock = sock
        self.addr = addr

    def send(self, data: bytes):
        self._sock.sendto(data, self.addr)

    def recv(self, bufsize: int = 65536) -> bytes:
        data, _ = self._sock.recvfrom(bufsize)
        return data
