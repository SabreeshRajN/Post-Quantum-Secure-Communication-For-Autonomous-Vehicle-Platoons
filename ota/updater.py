"""Verifies a firmware signature before installing."""

from dataclasses import dataclass
from crypto.dilithium_sign import DilithiumSigner, SignatureError

class UpdateRejected(Exception):
    pass

@dataclass
class FirmwareUpdate:
    version: str
    image: bytes
    signature: bytes

def install_update(update: FirmwareUpdate, ota_public_key: bytes) -> str:
    signer = DilithiumSigner()
    payload = update.version.encode() + b"|" + update.image
    try:
        signer.verify_or_raise(ota_public_key, payload, update.signature)
    except SignatureError as e:
        raise UpdateRejected(f"Firmware signature invalid: {e}") from e
    
    return f"Successfully installed firmware {update.version}"
