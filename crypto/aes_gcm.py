"""AES-256-GCM encrypt/decrypt with associated data."""

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt(key: bytes, plaintext: bytes, aad: bytes = None) -> bytes:
    """Encrypts plaintext and returns (nonce + ciphertext)."""
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, aad)
    return nonce + ciphertext

def decrypt(key: bytes, payload: bytes, aad: bytes = None) -> bytes:
    """Decrypts (nonce + ciphertext) back to plaintext."""
    nonce, ciphertext = payload[:12], payload[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, aad)
