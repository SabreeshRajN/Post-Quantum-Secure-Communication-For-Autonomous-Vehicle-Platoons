"""Derive the AES session key from the Kyber secret."""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

def derive_session_key(shared_secret: bytes, transcript: bytes = None) -> bytes:
    """Derives a 32-byte AES-256 session key from the shared secret."""
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=transcript,
        info=b"vehicle-platoon-session"
    )
    return hkdf.derive(shared_secret)
