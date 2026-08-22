"""Ed25519 agent identity binding (Project 4 / Zero Trust)."""

from __future__ import annotations

from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
    load_pem_private_key,
)

KEYS = Path(__file__).resolve().parent / "keys"
PRIV = KEYS / "orchestrator_ed25519.pem"
PUB = KEYS / "orchestrator_ed25519.pub"


def ensure_keys() -> None:
    KEYS.mkdir(parents=True, exist_ok=True)
    if PRIV.exists() and PUB.exists():
        return
    key = Ed25519PrivateKey.generate()
    PRIV.write_bytes(
        key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
    )
    PUB.write_bytes(key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw))


def load_private() -> Ed25519PrivateKey:
    ensure_keys()
    loaded = load_pem_private_key(PRIV.read_bytes(), password=None)
    if not isinstance(loaded, Ed25519PrivateKey):
        raise TypeError("Expected Ed25519 private key")
    return loaded


def sign_message(body: str) -> str:
    return load_private().sign(body.encode("utf-8")).hex()


def verify_message(body: str, signature_hex: str) -> bool:
    ensure_keys()
    public = Ed25519PublicKey.from_public_bytes(PUB.read_bytes())
    try:
        public.verify(bytes.fromhex(signature_hex), body.encode("utf-8"))
        return True
    except (InvalidSignature, ValueError):
        return False
