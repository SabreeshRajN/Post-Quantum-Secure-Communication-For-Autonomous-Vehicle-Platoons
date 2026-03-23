from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class SessionKeyDerivation:

    def derive_session_key(self, shared_secret):

        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit session key
            salt=None,
            info=b"vehicle-platoon-session",
            backend=default_backend()
        )

        session_key = hkdf.derive(shared_secret)

        return session_key