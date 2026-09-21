"""Encrypted, replay-protected message channel."""

import struct
from crypto import aes_gcm

class ReplayError(Exception):
    pass

class Session:
    def __init__(self, key: bytes, check_replay: bool = True):
        self._key = key
        self._check_replay = check_replay
        self._tx_seq = 0
        self._rx_seq = -1

    def encrypt(self, payload: bytes) -> bytes:
        """Encrypts payload with sequence number to prevent replay."""
        seq_bytes = struct.pack(">q", self._tx_seq)
        self._tx_seq += 1
        message = seq_bytes + payload
        return aes_gcm.encrypt(self._key, message)

    def decrypt(self, packet: bytes) -> tuple[bytes, int, bytes]:
        """Decrypts packet, checks sequence number. Returns (payload, seq, key)."""
        message = aes_gcm.decrypt(self._key, packet)
        seq = struct.unpack_from(">q", message, 0)[0]
        payload = message[8:]
        
        if self._check_replay:
            if seq <= self._rx_seq:
                raise ReplayError(f"Replay detected: seq {seq} <= {self._rx_seq}")
            self._rx_seq = seq
            
        return payload, seq, self._key
