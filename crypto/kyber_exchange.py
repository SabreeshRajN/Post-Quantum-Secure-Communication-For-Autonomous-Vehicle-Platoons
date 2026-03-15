from pqcrypto.kem.ml_kem_768 import generate_keypair, encrypt, decrypt


class KyberKeyExchange:

    def generate_keypair(self):
        public_key, secret_key = generate_keypair()
        return public_key, secret_key

    def encapsulate(self, public_key):
        ciphertext, shared_secret = encrypt(public_key)
        return ciphertext, shared_secret

    def decapsulate(self, secret_key, ciphertext):
        shared_secret = decrypt(secret_key, ciphertext)
        return shared_secret