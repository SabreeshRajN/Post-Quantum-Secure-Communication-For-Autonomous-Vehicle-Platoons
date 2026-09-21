"""Dilithium (ML-DSA) signatures."""

import config
from pqcrypto import InvalidSignatureError

class SignatureError(Exception):
    pass

class DilithiumSigner:
    def __init__(self):
        self._sig = config.load_sig()

    def generate_keypair(self):
        # returns (public_key, private_key)
        return self._sig.keygen()

    def sign(self, private_key: bytes, message: bytes) -> bytes:
        return self._sig.sign(private_key, message)

    def verify_or_raise(self, public_key: bytes, message: bytes, signature: bytes):
        """Verifies the signature, raises SignatureError if invalid."""
        try:
            self._sig.verify(public_key, message, signature)
        except InvalidSignatureError as e:
            raise SignatureError("Invalid signature") from e
