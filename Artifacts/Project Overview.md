# Capstone Project — Post-Quantum Secure V2V Platoon Communication
 
**Folder:** `D:\My Projects\Capstone Project` (Windows, device "sabreesh")
**Team 11** — Varshini B M, Mohammed Shaahid, Khalvathy A, Sabreesh Raj N
Dept. of CSE (AI/ML), Sri Krishna College of Technology, Coimbatore. Guided by Dr. Suma Sira Jacob.
 
Related paper submission (National Academy Science Letters, via Editorial Manager) is titled
"Quantum-Resistant Vehicle-to-Vehicle Platoon Communication System Using Post-Quantum Cryptography" —
co-authors there: Suma Sira Jacob, Sabreesh Raj N, Varshini B M, Mohammed Shaahid A.
 
## What it is
A Python simulation of a quantum-resistant V2V (vehicle-to-vehicle) platoon: one **leader** vehicle
and *N* **follower** vehicles communicating over UDP on loopback, mutually authenticated and
encrypted end-to-end with NIST-standard post-quantum algorithms. It extends a base paper
("Quantum-resistant Transport Layer Security", García et al., 2024, hybrid QKD+PQC over TLS) by
dropping QKD/optical fiber entirely and using a **pure post-quantum** channel suited to a moving
vehicle — no specialized hardware.
 
## Crypto stack
| Purpose | Algorithm |
|---|---|
| Identity / certificates | Dilithium3 (ML-DSA-65) |
| Key exchange | Kyber-768 (ML-KEM-768) |
| Session encryption | AES-256-GCM |
| Session key derivation | HKDF-SHA256 |
 
Crypto-agile: `config.py` centralizes the algorithm choice (`KEM_ALGORITHM`, `SIG_ALGORITHM`) with
alternate parameter sets available for benchmarking (Kyber-512/768/1024, Dilithium 2/3/5).
Uses the `pqcrypto` PyPI package (PQClean/Rust bindings) — explicitly NOT the unrelated `oqs` package
that was previously mistaken for liboqs (noted as a past bug in requirements.txt comments).
 
## Handshake protocol
A mini Certificate Authority (`identity/pki.py`) issues every vehicle a Dilithium-signed identity.
Leader and each follower then run a 3-message mutual-auth handshake:
```
1. leader   -> follower : Hello + Nonce
2. follower -> leader   : Follower Cert + Kyber public key + Signature
3. leader   -> follower : Leader Cert + Kyber ciphertext + Signature
```
Both signatures cover the nonce (binds the exchange, rejects replays). Leader encapsulates a shared
secret against the follower's Kyber-768 key; both derive an AES-256-GCM session key via HKDF-SHA256.
Every platoon command afterward is one AEAD-encrypted UDP datagram; RTT is measured per ack.
 
## Project layout
- `main.py` — interactive leader + N-follower live simulation (`python main.py [N]`)
- `demo.py` — narrated walkthrough incl. attack scenarios: `handshake`, `mitm` (identity checks on/off),
  `replay`, `tamper`, `firmware`
- `identity/pki.py` — mini CA
- `crypto/` — `kyber_exchange.py`, `dilithium_sign.py`, `aes_gcm.py`, `hkdf_session.py`
- `protocol/` — `handshake.py`, `session.py` (sequence-number replay protection), `wire.py`
- `vehicles/vehicle.py` — UDP handshake + secure command channel per vehicle
- `attacks/mitm.py` — standalone MITM attacker (used by the demo)
- `ota/` — `ota_server.py`, `updater.py` — Dilithium-signed firmware update demo
- `utils/telemetry.py`, `utils/console.py` — RTT/crypto-timing benchmark + console output
- `dashboard/` — live web dashboard: FastAPI + WebSocket backend (`dashboard/backend/app.py`,
  `event_bus.py`) pushing scenario events to a React/Vite frontend (`dashboard/frontend/`, Tailwind);
  `/api/scenario/{name}` triggers a demo scenario thread, `/ws` streams events
- `Claude Design/V2V Platoon Monitor.dc.html` — a design-canvas mockup of a platoon monitor UI
- `Artifacts/` — base paper PDF, comparison PDF, and 3 versions of the capstone PPT deck
- `SystemArchitecture.pdf` — original handshake diagram
- `benchmark/` — timing results dir (generated at runtime, gitignored, currently empty)
## Key design principles
- Fail-safe auth: `DilithiumSigner.verify_or_raise` prevents silently ignoring a failed signature check
- Each primitive maps to a specific threat: Kyber → eavesdropping, Dilithium → MITM/impersonation,
  AES-GCM → tampering, Session sequence numbers → replay
## Acknowledged limitations (from README)
- Dilithium3 certs exceed the standard 1500-byte Ethernet MTU (~vs 784 bytes for RSA) — real
  deployments would need handshake fragmentation or lighter parameter sets for latency-critical msgs
- Pure-Python crypto cost — a production system would want hardware-accelerated PQC (e.g. ESP32)
- No RF/road validation — runs over loopback UDP on one machine only; out of scope per lit survey
## Running it
```
python -m venv env && env\Scripts\activate
pip install -r requirements.txt
python main.py            # 1 leader + 2 followers
python demo.py mitm off   # attack demo, identity checks disabled -- succeeds
```
 
## Notes for future sessions
- No local shell (`device_bash`) was available when this was written; contents were read via
  `device_list_dir` + `device_stage_files`, not run/tested.
- `env/` is a Python venv (large, ignore when browsing); `dashboard/frontend/` has its own
  `node_modules`-style build (`dist/`) — both are noise for code review, not source.