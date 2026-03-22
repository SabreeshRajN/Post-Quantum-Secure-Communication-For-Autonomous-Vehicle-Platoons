import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AESGCMCipher:

    def __init__(self, key):
        """
        Initialize AES-256-GCM cipher with a 32-byte key.
        The key is the raw shared secret from Kyber KEM.
        """
        self.aesgcm = AESGCM(key)

    def encrypt(self, plaintext):
        """
        Encrypt plaintext bytes using AES-256-GCM.
        Returns (nonce, ciphertext) tuple.
        """
        nonce = os.urandom(12)  # 96-bit nonce recommended for GCM
        ciphertext = self.aesgcm.encrypt(nonce, plaintext, None)
        return nonce, ciphertext

    def decrypt(self, nonce, ciphertext):
        """
        Decrypt ciphertext bytes using AES-256-GCM.
        Returns the original plaintext bytes.
        """
        plaintext = self.aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext
