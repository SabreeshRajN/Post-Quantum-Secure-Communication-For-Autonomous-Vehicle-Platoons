# Post-Quantum Secure V2V Platoon Codebase Analysis

The codebase is a working prototype of a quantum-resistant vehicle-to-vehicle (V2V) platoon simulation, designed to protect communications between a **leader** vehicle and multiple **follower** vehicles against both classical and future quantum computer attacks.

## Architecture Overview

The system is built around a centralized leader that broadcasts driving commands to followers over UDP. It provides a secure channel establishing identity, preventing eavesdropping, tampering, impersonation, and replay attacks.

### 1. Cryptographic Stack (`crypto/`)
The project utilizes the `pqcrypto` library for post-quantum primitives and standard libraries for symmetric encryption.
*   **Key Exchange (KEM)**: Uses **Kyber (ML-KEM)** (`crypto/kyber_exchange.py`) to establish a shared secret over an insecure channel.
*   **Authentication**: Uses **Dilithium (ML-DSA)** (`crypto/dilithium_sign.py`) for digital signatures. This ensures that the Kyber keys are bound to a verified vehicle identity.
*   **Symmetric Encryption**: Uses **AES-256-GCM** (`crypto/aes_gcm.py`) for encrypting the actual commands sent between vehicles. It provides both confidentiality and message integrity (tamper detection).
*   **Key Derivation**: Uses **HKDF** (`crypto/hkdf_session.py`) to derive the AES session key from the Kyber shared secret.

### 2. Identity and PKI (`identity/`)
*   `identity/pki.py`: Implements a mini Certificate Authority (CA). During initialization, each vehicle (leader and followers) is issued a certificate. This certificate binds their identity (e.g., `follower-1`) to their Dilithium public key, signed by the CA.

### 3. Protocol Implementation (`protocol/`)
*   `protocol/handshake.py`: The core of the secure setup. It orchestrates a 3-step authenticated handshake:
    1.  Leader sends a HELLO with a random nonce.
    2.  Follower replies with its certificate, an ephemeral Kyber public key, and signs the payload with its Dilithium identity key.
    3.  Leader verifies the follower, encapsulates a shared secret, and signs the transcript with its own identity key.
*   `protocol/session.py`: Manages the active encrypted session post-handshake. It uses AES-256-GCM to encrypt/decrypt payloads and tracks sequence numbers to detect and block **replay attacks**.
*   `protocol/wire.py`: Provides simple pack/unpack utilities for structuring UDP payloads.

### 4. Over-The-Air (OTA) Updates (`ota/`)
*   `ota/ota_server.py` & `ota/updater.py`: Demonstrates secure firmware updates. The server signs the firmware image with a Dilithium signature, and the updater strictly verifies it before "installation," preventing malicious firmware injection.

### 5. Crypto Agility (`config.py`)
The system is built to be "crypto-agile". `config.py` acts as a central configuration file allowing you to swap out parameter sets (e.g., switching from Kyber-768 to Kyber-1024 or Dilithium3 to Dilithium5) with a single line change.

### 6. Executables & Scenarios
*   `main.py`: The live interactive simulation. It provisions certificates, spins up follower threads as UDP servers, connects the leader, and drops you into a prompt to type commands (e.g., "SET GAP 20m"). It records RTT telemetry and displays a benchmark dashboard on exit.
*   `demo.py`: A very useful script showcasing various attack scenarios and how the system defends against them:
    *   `handshake`: Demonstrates the secure session setup.
    *   `mitm`: Demonstrates a Man-In-The-Middle attack. When secure mode is ON, Dilithium signatures block it. When OFF, the attacker intercepts and modifies commands.
    *   `replay`: Captures a packet and resends it. `Session` sequence numbers block it.
    *   `tamper`: Modifies a bit in transit. AES-GCM tags catch the modification.
    *   `firmware`: Shows the OTA update rejecting a forged firmware image.

## Key Design Principles
*   **Fail-Safe Authentication**: The `DilithiumSigner` explicitly implements a `verify_or_raise` method to prevent developers from accidentally ignoring a `False` return value from a signature check.
*   **Threat Modeling**: The code maps each cryptographic primitive directly to a specific threat (Kyber for eavesdropping, Dilithium for MITM/Impersonation, AES-GCM for tampering, Session sequences for replay).
