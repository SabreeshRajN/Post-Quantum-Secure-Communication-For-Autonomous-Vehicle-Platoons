"""Signs firmware updates."""

from crypto.dilithium_sign import DilithiumSigner

class OtaServer:
    def __init__(self):
        self._signer = DilithiumSigner()
        self.public_key, self._private_key = self._signer.generate_keypair()

    def publish(self, version: str, image: bytes):
        from ota.updater import FirmwareUpdate
        payload = version.encode() + b"|" + image
        signature = self._signer.sign(self._private_key, payload)
        return FirmwareUpdate(version, image, signature)
