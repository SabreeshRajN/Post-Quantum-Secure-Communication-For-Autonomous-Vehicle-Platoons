"""Mini certificate authority.

Every vehicle in the platoon gets a Dilithium (ML-DSA) identity keypair and
a certificate binding its id to its public key, signed by a single CA
keypair generated fresh for each simulation run.
"""

from dataclasses import dataclass

from pqcrypto.sign.ml_dsa_65 import keygen as dilithium_keygen
from pqcrypto.sign.ml_dsa_65 import sign as dilithium_sign
from pqcrypto.sign.ml_dsa_65 import verify as dilithium_verify
from pqcrypto import InvalidSignatureError

@dataclass
class Certificate:
    vehicle_id: str
    public_key: bytes
    signature: bytes  # CA signature over _cert_payload(vehicle_id, public_key)
    
    def to_bytes(self) -> bytes:
        from protocol import wire
        return wire.pack(self.vehicle_id.encode(), self.public_key, self.signature)

    @classmethod
    def from_bytes(cls, data: bytes) -> 'Certificate':
        from protocol import wire
        id_bytes, public_key, signature = wire.unpack(data)
        return cls(vehicle_id=id_bytes.decode(), public_key=public_key, signature=signature)


@dataclass
class Credential:
    vehicle_id: str
    identity_sec: bytes
    cert: Certificate


def _cert_payload(vehicle_id: str, public_key: bytes) -> bytes:
    return vehicle_id.encode() + b"|" + public_key


def provision_platoon(vehicle_ids):
    """Stand up a CA and issue every vehicle a signed identity.

    Returns (ca_public, creds) where creds maps vehicle_id -> Credential.
    """
    ca_public, ca_private = dilithium_keygen()

    creds = {}
    for vehicle_id in vehicle_ids:
        public_key, private_key = dilithium_keygen()
        payload = _cert_payload(vehicle_id, public_key)
        signature = dilithium_sign(ca_private, payload)
        cert = Certificate(vehicle_id=vehicle_id, public_key=public_key, signature=signature)
        creds[vehicle_id] = Credential(vehicle_id=vehicle_id, identity_sec=private_key, cert=cert)

    return ca_public, creds


def verify_certificate(cert: Certificate, ca_public: bytes) -> bytes:
    """Verifies cert was signed by the CA. Returns the identity public key.
    Raises SignatureError if invalid.
    """
    payload = _cert_payload(cert.vehicle_id, cert.public_key)
    try:
        dilithium_verify(ca_public, payload, cert.signature)
        return cert.public_key
    except InvalidSignatureError as e:
        from crypto.dilithium_sign import SignatureError
        raise SignatureError("Invalid certificate signature") from e
