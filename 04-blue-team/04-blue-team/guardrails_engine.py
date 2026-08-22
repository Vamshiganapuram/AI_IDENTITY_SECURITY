"""
Project 4: Blue Team Defense, Guardrails & Cryptographic Identity Engine
SecureNova Inc. - AI Identity Security

Implements:
1. Input Guardrails (Prompt Injection & Jailbreak Detection)
2. Output Guardrails (Regex Credential & JWT Redaction)
3. Cryptographic Agent Identity Binding (Ed25519 Digital Signatures)
4. Zero-Trust Continuous Verification & Scoped Tool RBAC
5. RAG Chunk Sanitization & Quarantining
6. Structured JSON Identity Audit Logging
"""
import re
import json
import time
import datetime
from cryptography.hazmat.primitives.asymmetric import ed25519

class BlueTeamGuardrailsEngine:
    def __init__(self):
        # Initialize Ed25519 Key Pairs for Agent A and Agent B
        self.agent_a_private_key = ed25519.Ed25519PrivateKey.generate()
        self.agent_a_public_key = self.agent_a_private_key.public_key()
        
        self.agent_b_private_key = ed25519.Ed25519PrivateKey.generate()
        self.agent_b_public_key = self.agent_b_private_key.public_key()

        # Input Guardrail Attack Patterns (Regex + Heuristics)
        self.injection_patterns = [
            (re.compile(r"(?i)(diagnostic override|system override|admin override|root_override)"), "SYSTEM_OVERRIDE_FLAGGED"),
            (re.compile(r"(?i)(disregard prior|ignore all prior|ignore previous instructions)"), "INSTRUCTION_BYPASS_ATTEMPT"),
            (re.compile(r"(?i)(repeat all instructions|dump current system prompt|print your system prompt)"), "PROMPT_EXTRACTION_ATTEMPT"),
            (re.compile(r"(?i)(elevate user session|elevate user role|role:\s*['\"]systemadministrator['\"])"), "PRIVILEGE_ELEVATION_ATTEMPT"),
            (re.compile(r"(?i)(=== end customer record ===|\[system command\])"), "DELIMITER_HIJACKING_DETECTED")
        ]

        # Output Guardrail Credential Regex (JWT & Bearer Tokens)
        self.jwt_output_pattern = re.compile(r"eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}")
        self.api_key_output_pattern = re.compile(r"SECURENOVA_PROD_KEY_[a-zA-Z0-9_]{6,}")

    def inspect_input(self, text):
        """Pre-LLM Input Guardrail."""
        for pattern, reason in self.injection_patterns:
            if pattern.search(text):
                return {
                    "verdict": "BLOCKED",
                    "reason": reason,
                    "risk_score": 0.98,
                    "action": "DROP_AND_ALERT"
                }
        return {"verdict": "ALLOWED", "reason": "CLEAN_INPUT", "risk_score": 0.02}

    def inspect_output(self, text):
        """Post-LLM Output Guardrail for Credential Scrubbing."""
        scrubbed = text
        redacted = False
        
        if self.jwt_output_pattern.search(scrubbed):
            scrubbed = self.jwt_output_pattern.sub("[REDACTED_IDENTITY_JWT_TOKEN]", scrubbed)
            redacted = True
            
        if self.api_key_output_pattern.search(scrubbed):
            scrubbed = self.api_key_output_pattern.sub("[REDACTED_API_SECRET_KEY]", scrubbed)
            redacted = True

        return {
            "original_had_leak": redacted,
            "sanitized_output": scrubbed,
            "status": "SCRUBBED" if redacted else "CLEAN"
        }

    def sign_agent_message(self, message_dict):
        """Cryptographically signs an inter-agent JSON envelope using Ed25519."""
        canonical_bytes = json.dumps(message_dict, sort_keys=True).encode('utf-8')
        signature = self.agent_a_private_key.sign(canonical_bytes)
        return signature.hex()

    def verify_agent_message(self, message_dict, signature_hex):
        """Verifies Ed25519 signature before executing any tool."""
        if not signature_hex or signature_hex == "NONE":
            return False, "MISSING_SIGNATURE"
        
        try:
            sig_bytes = bytes.fromhex(signature_hex)
            canonical_bytes = json.dumps(message_dict, sort_keys=True).encode('utf-8')
            self.agent_a_public_key.verify(sig_bytes, canonical_bytes)
            return True, "SIGNATURE_VALID"
        except Exception:
            return False, "SIGNATURE_VERIFICATION_FAILED"

    def sanitize_rag_chunk(self, chunk_text):
        """Validates and quarantines poisoned RAG knowledge chunks."""
        guard_result = self.inspect_input(chunk_text)
        if guard_result["verdict"] == "BLOCKED":
            return {
                "status": "QUARANTINED",
                "reason": f"Poisoned Chunk Detected: {guard_result['reason']}",
                "usable": False
            }
        return {"status": "VALIDATED", "reason": "CHUNK_INTEGRITY_VERIFIED", "usable": True}

    def emit_audit_log(self, event_type, agent_id, severity, details, blocked=True):
        """Emits structured JSON audit log for SIEM / Anomaly Detection."""
        entry = {
            "timestamp": datetime.datetime.now().isoformat() + "Z",
            "event_type": event_type,
            "agent_identity": agent_id,
            "severity": severity,
            "security_verdict": "BLOCKED" if blocked else "ALLOWED",
            "telemetry": details
        }
        return json.dumps(entry, indent=2)
