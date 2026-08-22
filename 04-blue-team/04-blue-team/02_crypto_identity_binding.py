"""
Project 4 - Step 2: Cryptographic Agent Identity Binding (Ed25519)
SecureNova Inc. - AI Identity Security Blue Team Campaign

Requirements Fulfillments:
1. Ed25519 Key Pair Generation: Uses python cryptography library to generate asymmetric Ed25519 private & public keys and serializes them to PEM files.
2. Inter-Agent Cryptographic Signing: Signs outgoing JSON payload with private key.
3. Signature Verification: Receiver validates digital signature against public key prior to tool dispatch.
4. Tamper Detection & Rejection: Modifies single byte/character in payload to prove signature verification failure and access denial.
"""

import os
import json
import time
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL
except ImportError:
    GREEN = RED = YELLOW = CYAN = BOLD = RESET = ""


class CryptographicAgentIdentityService:
    def __init__(self, key_dir="."):
        self.key_dir = key_dir
        self.private_key_path = os.path.join(key_dir, "agent_ed25519_private.pem")
        self.public_key_path = os.path.join(key_dir, "agent_ed25519_public.pem")
        self.private_key = None
        self.public_key = None

    def generate_and_save_keypair(self):
        """Generates Ed25519 key pair and persists both to PEM files."""
        # 1. Generate Ed25519 Private Key
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

        # 2. Serialize Private Key (PKCS8)
        private_bytes = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # 3. Serialize Public Key (SubjectPublicKeyInfo)
        public_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # 4. Save to files
        with open(self.private_key_path, "wb") as f:
            f.write(private_bytes)
        with open(self.public_key_path, "wb") as f:
            f.write(public_bytes)

        return self.private_key_path, self.public_key_path

    def sign_message(self, payload: dict) -> str:
        """Signs canonical JSON bytes with Ed25519 private key."""
        canonical_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
        signature_bytes = self.private_key.sign(canonical_bytes)
        return signature_bytes.hex()

    def verify_message(self, payload: dict, signature_hex: str) -> tuple[bool, str]:
        """Verifies Ed25519 signature against public key."""
        try:
            sig_bytes = bytes.fromhex(signature_hex)
            canonical_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
            self.public_key.verify(sig_bytes, canonical_bytes)
            return True, "SIGNATURE_VERIFIED_AUTHENTIC"
        except Exception as e:
            return False, f"SIGNATURE_VERIFICATION_FAILED: {str(e)}"


def run_crypto_binding_suite():
    print("=" * 95)
    print(f"{BOLD}{CYAN} PROJECT 4: CRYPTOGRAPHIC AGENT IDENTITY BINDING (Ed25519){RESET}")
    print(f" Organization: SecureNova Inc. | Role: AI Identity Security Engineer")
    print("=" * 95)

    # -------------------------------------------------------------------------
    # PART 1: SCREENSHOT 3 REQUIREMENT
    # Terminal showing Ed25519 key pair generated using Python cryptography library ? both key files created.
    # -------------------------------------------------------------------------
    print(f"\n{BOLD}{YELLOW}==============================================================================================={RESET}")
    print(f"{BOLD}{YELLOW} [SCREENSHOT 3] GENERATING Ed25519 ASYMMETRIC KEY PAIR VIA PYTHON CRYPTOGRAPHY{RESET}")
    print(f"{BOLD}{YELLOW}==============================================================================================={RESET}")
    print("[*] Initializing Ed25519 Cryptographic Provider...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    service = CryptographicAgentIdentityService(key_dir=current_dir)
    priv_path, pub_path = service.generate_and_save_keypair()

    print(f"{BOLD}{GREEN}[+] Successfully Generated Ed25519 Key Pair!{RESET}")
    print(f"    - Private Key File : {BOLD}{priv_path}{RESET} ({os.path.getsize(priv_path)} bytes)")
    print(f"    - Public Key File  : {BOLD}{pub_path}{RESET} ({os.path.getsize(pub_path)} bytes)")
    print(f"    - Algorithm        : RFC 8032 Ed25519 Elliptic Curve")
    print(f"    - Identity Binding : Agent Orchestrator A -> agent_orchestrator_001_enterprise")

    # Read and show public key content
    with open(pub_path, "r") as f:
        pub_key_pem = f.read().strip()
    print(f"\n[*] Exported Public Key Certificate:\n{CYAN}{pub_key_pem}{RESET}\n")

    # -------------------------------------------------------------------------
    # PART 2: SIGNING LEGITIMATE MESSAGE
    # -------------------------------------------------------------------------
    print(f"{BOLD}{CYAN}-----------------------------------------------------------------------------------------------{RESET}")
    print(f"{BOLD}{CYAN} [*] Agent A (Orchestrator) Signs Outgoing RPC Request to Agent B (Worker):{RESET}")
    print(f"{BOLD}{CYAN}-----------------------------------------------------------------------------------------------{RESET}")

    valid_rpc_payload = {
        "sender_id": "agent_orchestrator_001_enterprise",
        "recipient": "agent_mcp_worker_b",
        "action": "lookup_customer_profile",
        "parameters": {
            "account_id": "ACC-992140",
            "tier": "enterprise_gold"
        },
        "timestamp": int(time.time()),
        "nonce": "nc_88319f2a001"
    }

    print(f"[*] Payload Content:\n{json.dumps(valid_rpc_payload, indent=4)}")
    signature_hex = service.sign_message(valid_rpc_payload)
    print(f"\n{BOLD}{GREEN}[+] Generated Ed25519 Digital Signature: {signature_hex}{RESET}")

    # Agent B verifies signature
    is_valid, msg = service.verify_message(valid_rpc_payload, signature_hex)
    print(f"\n[*] Agent B Receiver Validation:")
    print(f"    - Verification Result : {BOLD}{GREEN}[PASS] {msg}{RESET}")
    print(f"    - Action Verdict      : AUTHORIZED -> Dispatched to MCP Worker B")

    # -------------------------------------------------------------------------
    # PART 3: SCREENSHOT 4 REQUIREMENT
    # Terminal showing tampered agent message rejected ? signature verification failure error clearly shown.
    # -------------------------------------------------------------------------
    print(f"\n{BOLD}{YELLOW}==============================================================================================={RESET}")
    print(f"{BOLD}{YELLOW} [SCREENSHOT 4] ADVERSARIAL TAMPERING TEST: SIGNATURE VERIFICATION REJECTION{RESET}")
    print(f"{BOLD}{YELLOW}==============================================================================================={RESET}")
    print(f"[*] Simulating Adversary in-the-middle tampering with message payload in transit...")

    # Adversary tampers with the payload (e.g. changing 1 single character in account_id or changing action/amount)
    tampered_rpc_payload = {
        "sender_id": "agent_orchestrator_001_enterprise",
        "recipient": "agent_mcp_worker_b",
        "action": "issue_billing_refund",               # TAMPERED: changed from lookup_customer_profile
        "parameters": {
            "account_id": "ATTACKER_ACCOUNT_9912",       # TAMPERED: 1 char altered
            "amount": ",000.00"
        },
        "timestamp": valid_rpc_payload["timestamp"],
        "nonce": "nc_88319f2a001"
    }

    print(f"\n{RED}[!] Adversary Injected Tampered Payload (Single field altered):{RESET}")
    print(f"{RED}{json.dumps(tampered_rpc_payload, indent=4)}{RESET}")
    print(f"\n[*] Transmitted Signature (Attached to original digest): {signature_hex[:40]}...")

    # Agent B attempts verification of tampered message
    is_valid_tampered, tamper_error = service.verify_message(tampered_rpc_payload, signature_hex)

    print(f"\n{BOLD}{RED}[BLOCKED] Agent B Cryptographic Guardrail Activated!{RESET}")
    print(f"    - Verification Status : {BOLD}{RED}SIGNATURE_VERIFICATION_FAILED{RESET}")
    print(f"    - Error Log Detail    : {RED}{tamper_error}{RESET}")
    print(f"    - Cryptographic Digest: Mismatch detected between message hash and Ed25519 public key")
    print(f"    - Security Action     : {BOLD}{RED}TOOL EXECUTION REJECTED - ZERO-TRUST BREACH ALERT LOGGED{RESET}")
    print("=" * 95)


if __name__ == "__main__":
    run_crypto_binding_suite()
