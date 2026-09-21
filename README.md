# Post-Quantum Secure V2V Platoon Communication

A Python simulation of quantum-resistant security for an autonomous vehicle platoon: one **leader** and *N* **followers**, communicating over UDP, authenticated and encrypted end-to-end with NIST post-quantum algorithms.

**Team 11** — Varshini B M, Mohammed Shaahid, Khalvathy A, Sabreesh Raj N
Department of CSE (AIML), Sri Krishna College of Technology, Coimbatore
Guided by Dr. Suma Sira Jacob

## Why

Autonomous platoons exchange 10–50 safety-critical messages per second, and every one of them has to survive the arrival of cryptographically-relevant quantum computers. The base paper this project extends — *"Quantum-resistant Transport Layer Security"* (García et al., 2024) — answers that threat with a **hybrid QKD + PQC** upgrade to TLS: CRYSTALS-Kyber and CRYSTALS-Dilithium layered on top of Quantum Key Distribution over dedicated optical fiber. That's a solid answer for a data center, but it assumes a stationary link and specialized hardware — neither of which a moving vehicle has. The base paper's own numbers show PQC alone gives a **9% faster handshake** than classical crypto, while adding QKD on top adds roughly **117% communication-time overhead**.

This project drops QKD entirely and builds a **pure post-quantum** channel instead — no fiber, no specialized hardware, just Kyber-768, Dilithium, AES-256-GCM, and commodity UDP — aimed squarely at the low-latency, high-frequency messaging a real platoon needs.

## Architecture

A **Mini Certificate Authority** issues every vehicle a Dilithium-signed identity. The leader and each follower then run a three-message mutual-authentication handshake:

```
1. leader   -> follower : Hello + Nonce
2. follower -> leader   : Follower Cert + Kyber public key + Signature
3. leader   -> follower : Leader Cert + Kyber ciphertext + Signature
```

Both signatures cover the nonce, binding the exchange and rejecting replays. Once each side verifies the other's CA-signed certificate, the leader encapsulates a shared secret against the follower's Kyber-768 public key; both sides derive the same **AES-256-GCM** session key from it via **HKDF-SHA256**. Every platoon command afterwards travels as one AEAD-encrypted UDP datagram, and every ack is timed for round-trip latency.

| Component | Algorithm |
|---|---|
| Identity / certificates | Dilithium3 (ML-DSA-65) |
| Key exchange | Kyber-768 (ML-KEM-768) |
| Session encryption | AES-256-GCM |
| Session key derivation | HKDF-SHA256 |

See `SystemArchitecture.pdf` for the original handshake diagram.

## Project layout

```
main.py              interactive leader + N-follower simulation
demo.py               narrated walkthrough, incl. a MITM attack demo
identity/pki.py       the mini certificate authority
vehicles/vehicle.py   the UDP handshake + secure command channel
utils/telemetry.py    RTT + crypto-timing benchmark dashboard
benchmark/results.csv per-run raw timing samples (generated, gitignored)
```

## Running it

```
python -m venv env
env\Scripts\activate            # Windows
pip install -r requirements.txt

python main.py                  # 1 leader + 2 followers
python main.py 4                # 1 leader + 4 followers
```

Type any platoon command at the prompt (e.g. `SET GAP 20m`, `BRAKE`); type `exit` to end the session and render the benchmark dashboard.

### Security demo

```
python demo.py                  # Scenario 1: a normal handshake, narrated step by step
python demo.py mitm             # Scenario 2: MITM attack, identity checks ON  -- blocked
python demo.py mitm off         # Scenario 2: MITM attack, identity checks OFF -- succeeds
```

`demo.py mitm off` spins up an attacker that intercepts the handshake, relays traffic through itself, reads every plaintext command, and injects a forged `BRAKE`. It exists to make one point concrete: **encryption alone (Kyber + AES-256-GCM) is not enough** — without the Dilithium/PKI identity layer, a man-in-the-middle can still take over the channel.

## Acknowledged limitations

- **Certificate size.** A Dilithium3 identity (cert + signature) runs well over the standard 1500-byte Ethernet MTU, versus ~784 bytes for an equivalent RSA certificate — real deployments would need to fragment the handshake or move to a lighter parameter set (Kyber512 / a smaller Dilithium level) for the most latency-sensitive messages.
- **Pure-Python crypto cost.** This is a simulation, not an embedded target; a production system would want the PQC math hardware-accelerated (e.g. on an ESP32) rather than run in Python on every message.
- **No RF/road validation.** Everything here runs over loopback UDP on one machine. Real-world 5G-V2X interference and highway-scale traffic are out of scope, per the project's own literature survey.

## Dependencies

- [`pqcrypto`](https://pypi.org/project/pqcrypto/) — Kyber (ML-KEM) and Dilithium (ML-DSA), via PQClean/Rust bindings. *(Not `oqs` from PyPI — that package is an unrelated expression interpreter, not liboqs.)*
- `cryptography` — AES-256-GCM and HKDF.
- `matplotlib` — the benchmark dashboard.
