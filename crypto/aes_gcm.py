import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AESGCMCipher:
    """
    AES-256-GCM symmetric encryption/decryption.
    Uses the 32-byte Kyber shared secret directly as the key.
    """

    def __init__(self, key: bytes):
        if len(key) != 32:
            raise ValueError("AES-256-GCM requires a 32-byte key.")
        self.aesgcm = AESGCM(key)

    def encrypt(self, plaintext: str) -> bytes:
        """
        Encrypts a plaintext string.
        Returns nonce (12 bytes) + ciphertext concatenated.
        """
        nonce = os.urandom(12)  # 96-bit random nonce
        ciphertext = self.aesgcm.encrypt(nonce, plaintext.encode(), None)
        return nonce + ciphertext  # prepend nonce for receiver

    def decrypt(self, payload: bytes) -> str:
        """
        Decrypts a payload of nonce + ciphertext.
        Returns the original plaintext string.
        """
        nonce = payload[:12]
        ciphertext = payload[12:]
        plaintext = self.aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode()
