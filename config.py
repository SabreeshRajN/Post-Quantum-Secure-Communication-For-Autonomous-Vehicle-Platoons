"""Central choice of post-quantum algorithms = "crypto agility".

Every wrapper loads its algorithm from here, so switching the whole platoon to a
different NIST security level is a ONE-LINE change. The benchmark harness uses the
option lists below to compare the parameter sets head-to-head.
"""

import importlib

# --- Defaults used by the running system ---------------------------------- #
KEM_ALGORITHM = "ml_kem_768"   # Kyber-768
SIG_ALGORITHM = "ml_dsa_65"    # Dilithium3

# --- All available options (for benchmarking / swapping) ------------------ #
KEM_OPTIONS = ["ml_kem_512", "ml_kem_768", "ml_kem_1024"]
SIG_OPTIONS = ["ml_dsa_44", "ml_dsa_65", "ml_dsa_87"]


def load_kem(name=None):
    return importlib.import_module(f"pqcrypto.kem.{name or KEM_ALGORITHM}")


def load_sig(name=None):
    return importlib.import_module(f"pqcrypto.sign.{name or SIG_ALGORITHM}")
