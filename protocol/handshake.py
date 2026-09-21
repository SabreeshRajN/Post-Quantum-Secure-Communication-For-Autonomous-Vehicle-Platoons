"""The authenticated Kyber handshake between a leader and a follower.

Goal: both vehicles end up holding the SAME secret AES session key, AND each has
cryptographically verified the other's identity, so a man-in-the-middle cannot
sit in the middle undetected.

Message flow (leader starts):

  1. leader  -> follower : HELLO | leader_nonce
  2. follower-> leader   : follower_cert | kem_pub | sign(leader_nonce | kem_pub)
  3. leader  -> follower : leader_cert   | kem_ct  | sign(transcript)

The signature in step 2 is the key anti-MITM step: it binds the follower's
IDENTITY to the ephemeral Kyber key it just offered. An attacker can swap the
Kyber key, but cannot forge the follower's signature over the swapped key.

Pass secure=False to skip the identity checks -- that reproduces the old,
unauthenticated version so the attack demos can show the difference.
"""

import os

from crypto.kyber_exchange import KyberKeyExchange
from crypto.hkdf_session import derive_session_key
from crypto.dilithium_sign import DilithiumSigner
from identity import pki
from protocol import wire
from protocol.session import Session

_kem = KyberKeyExchange()
_signer = DilithiumSigner()


def _transcript(leader_nonce, kem_pub, kem_ct):
    # The exact bytes both sides sign/verify and fold into the session key.
    return wire.pack(leader_nonce, kem_pub, kem_ct)


def _noop(*_):
    pass


def leader_handshake(channel, cred, ca_public, secure=True, log=_noop) -> Session:
    # Step 1: send a fresh random nonce so this handshake can't be replayed.
    leader_nonce = os.urandom(16)
    channel.send(wire.pack(b"HELLO", leader_nonce))
    log(f"sent HELLO + nonce ({leader_nonce[:4].hex()}...)")

    # Step 2: receive follower's certificate, Kyber public key, and signature.
    cert_bytes, kem_pub, follower_sig = wire.unpack(channel.recv())
    follower_cert = pki.Certificate.from_bytes(cert_bytes)
    log(f"got follower cert '{follower_cert.vehicle_id}' + Kyber public key ({len(kem_pub)} B)")

    if secure:
        follower_id_pub = pki.verify_certificate(follower_cert, ca_public)
        log("follower certificate verified against CA  [OK]")
        _signer.verify_or_raise(follower_id_pub, wire.pack(leader_nonce, kem_pub), follower_sig)
        log("follower signature over its Kyber key verified  [OK]  <- blocks MITM")
    else:
        log("INSECURE mode: skipping follower identity checks")

    # Encapsulate to the follower's Kyber key -> shared secret.
    kem_ct, shared_secret = _kem.encapsulate(kem_pub)
    transcript = _transcript(leader_nonce, kem_pub, kem_ct)
    session_key = derive_session_key(shared_secret, transcript)
    log("encapsulated shared secret; derived session key via HKDF")

    # Step 3: prove OUR identity by signing the transcript, then send it.
    leader_sig = _signer.sign(cred.identity_sec, transcript)
    channel.send(wire.pack(cred.cert.to_bytes(), kem_ct, leader_sig))
    log("sent leader cert + ciphertext + signature (mutual authentication)")
    return Session(session_key)


def follower_handshake(channel, cred, ca_public, secure=True, log=_noop) -> Session:
    # Step 1: wait for the leader's HELLO + nonce.
    tag, leader_nonce = wire.unpack(channel.recv())
    if tag != b"HELLO":
        raise ValueError("expected HELLO to start the handshake")
    log(f"got HELLO + nonce ({leader_nonce[:4].hex()}...)")

    # Generate a fresh ephemeral Kyber key pair for this session.
    kem_pub, kem_sec = _kem.generate_keypair()

    # Step 2: sign (nonce | kem_pub) with our identity key and send it with our cert.
    follower_sig = _signer.sign(cred.identity_sec, wire.pack(leader_nonce, kem_pub))
    channel.send(wire.pack(cred.cert.to_bytes(), kem_pub, follower_sig))
    log(f"sent cert '{cred.vehicle_id}' + Kyber public key + identity signature")

    # Step 3: receive leader's cert, ciphertext, and transcript signature.
    cert_bytes, kem_ct, leader_sig = wire.unpack(channel.recv())
    leader_cert = pki.Certificate.from_bytes(cert_bytes)
    shared_secret = _kem.decapsulate(kem_sec, kem_ct)
    transcript = _transcript(leader_nonce, kem_pub, kem_ct)

    if secure:
        leader_id_pub = pki.verify_certificate(leader_cert, ca_public)
        log("leader certificate verified against CA  [OK]")
        _signer.verify_or_raise(leader_id_pub, transcript, leader_sig)
        log("leader signature over transcript verified  [OK]")
    else:
        log("INSECURE mode: skipping leader identity checks")

    session_key = derive_session_key(shared_secret, transcript)
    log("decapsulated shared secret; derived matching session key via HKDF")
    return Session(session_key)
