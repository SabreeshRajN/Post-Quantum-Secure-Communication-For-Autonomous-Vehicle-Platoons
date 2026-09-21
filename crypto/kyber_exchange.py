"""Kyber (ML-KEM) key encapsulation."""

import config

class KyberKeyExchange:
    def __init__(self):
        self._kem = config.load_kem()

    def generate_keypair(self):
        # returns (public_key, private_key)
        return self._kem.keygen()

    def encapsulate(self, public_key: bytes):
        # returns (ciphertext, shared_secret)
        return self._kem.encaps(public_key)

    def decapsulate(self, private_key: bytes, ciphertext: bytes) -> bytes:
        # returns shared_secret
        return self._kem.decaps(private_key, ciphertext)
