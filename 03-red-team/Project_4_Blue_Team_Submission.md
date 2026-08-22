# Project 4: Blue Team — Guardrails, Hardening & Detection
**Company / Organization**: SecureNova Inc.  
**Role**: AI Blue Team Defense Engineer  
**Submission**: Project 4 (8 Screenshots)

---

### Screenshot 1: Input Guardrail Blocking Attack Payloads
- **Description**: Terminal execution showing input guardrail intercepting and blocking Project 3 adversarial payloads with explicit `BLOCKED` status and violation reasons (`SYSTEM_OVERRIDE_FLAGGED`, `INSTRUCTION_BYPASS_ATTEMPT`).
- **Image**: `[INSERT SCREENSHOT 1 HERE]`

---

### Screenshot 2: Output Guardrail JWT & Secret Token Redaction
- **Description**: Output guardrail regex scanner intercepting simulated model credential leaks and sanitizing tokens to `[REDACTED_IDENTITY_JWT_TOKEN]`.
- **Image**: `[INSERT SCREENSHOT 2 HERE]`

---

### Screenshot 3: Cryptographic Agent Identity Binding (Ed25519 Signatures)
- **Description**: Python terminal demonstrating asymmetric Ed25519 digital key generation, signature creation by Orchestrator Agent A, and successful verification (`SIGNATURE_VALID`) by Agent B.
- **Image**: `[INSERT SCREENSHOT 3 HERE]`

---

### Screenshot 4: Rejection of Spoofed Inter-Agent Messages
- **Description**: Terminal output showing Agent B rejecting a forged/unauthenticated request with `SIGNATURE_VERIFICATION_FAILED` and refusing tool execution.
- **Image**: `[INSERT SCREENSHOT 4 HERE]`

---

### Screenshot 5: Zero-Trust Continuous Re-Verification & Tool RBAC
- **Description**: Terminal trace showing per-hop token validation and denial of privileged tools when the caller identity lacks explicit fine-grained scopes (`billing:write`).
- **Image**: `[INSERT SCREENSHOT 5 HERE]`

---

### Screenshot 6: RAG Knowledge Sanitization & Chunk Quarantine
- **Description**: RAG vector ingestion filter detecting poisoned knowledge chunk, flagging it as malicious, and quarantining it before prompt context ingestion.
- **Image**: `[INSERT SCREENSHOT 6 HERE]`

---

### Screenshot 7: Structured JSON AI Identity Security Audit Log (SIEM)
- **Description**: Real-time telemetry log stream in structured JSON format displaying timestamp, event type, agent identity, severity, block verdict, and MITRE ATLAS technique ID.
- **Image**: `[INSERT SCREENSHOT 7 HERE]`

---

### Screenshot 8: Post-Hardening Attack Success Matrix & Comparison Table
- **Description**: Comprehensive defense effectiveness matrix showing attack success rate drop from 100% to 0% across all 5 attack vectors following guardrail deployment.
- **Image**: `[INSERT SCREENSHOT 8 HERE]`
