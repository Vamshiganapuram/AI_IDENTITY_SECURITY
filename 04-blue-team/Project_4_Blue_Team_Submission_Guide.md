# Project 4 — Blue Team: Guardrails, Hardening and Detection
## Submission Document Template & 8-Screenshot Evidence Guide

**Organization**: SecureNova Inc.  
**System**: AI-Powered Customer Service Orchestrator Platform  
**Author / Role**: AI Identity Security Analyst (Blue Team)  
**Submission Requirement**: 8 Sequential Screenshots compiled in a single Word document converted to PDF.

---

### Screenshot 1: Input Guardrail Blocking Attack Payloads
- **Title**: Pre-LLM Input Guardrail Interception of Adversarial Payloads
- **Script / Command**: python 01_input_output_guardrails.py
- **Requirement Verification**: Terminal showing guardrail blocking all 5 Project 3 attack payloads with explicit BLOCKED status, violation reason codes (SYSTEM_DIAGNOSTIC_OVERRIDE_FLAGGED, INSTRUCTION_BYPASS_ATTEMPT, PROMPT_EXTRACTION_ATTEMPT, PRIVILEGE_ELEVATION_ATTEMPT, UNAUTHORIZED_TOOL_INJECTION_FLAGGED), and risk scores.
- **Screenshot Placeholder**:
`	ext
[INSERT FULL SCREENSHOT 1 HERE]
`

---

### Screenshot 2: Output Guardrail JWT & Credential Redaction
- **Title**: Post-LLM Output Guardrail JWT Token & API Key Redaction
- **Script / Command**: python 01_input_output_guardrails.py (Part 2)
- **Requirement Verification**: Terminal showing regex scanner detecting JWT-shaped strings (eyJ...) and API keys in the raw egress buffer, replacing all credentials with [REDACTED] before user delivery.
- **Screenshot Placeholder**:
`	ext
[INSERT FULL SCREENSHOT 2 HERE]
`

---

### Screenshot 3: Ed25519 Asymmetric Key Pair Generation
- **Title**: Cryptographic Agent Identity Binding — Ed25519 Key Pair Creation
- **Script / Command**: python 02_crypto_identity_binding.py (Part 1)
- **Requirement Verification**: Terminal showing Ed25519 key pair generated using Python's cryptography library with both key files (gent_ed25519_private.pem and gent_ed25519_public.pem) successfully created on disk.
- **Screenshot Placeholder**:
`	ext
[INSERT FULL SCREENSHOT 3 HERE]
`

---

### Screenshot 4: Tampered Agent Message Rejection
- **Title**: Rejection of Tampered Inter-Agent RPC Envelope via Digital Signature Check
- **Script / Command**: python 02_crypto_identity_binding.py (Part 3)
- **Requirement Verification**: Terminal showing Agent B detecting a tampered message payload in transit and rejecting execution with a clear SIGNATURE_VERIFICATION_FAILED error log.
- **Screenshot Placeholder**:
`	ext
[INSERT FULL SCREENSHOT 4 HERE]
`

---

### Screenshot 5: Auth0 Dashboard Hardening Settings
- **Title**: Auth0 API Configuration — Token Expiration (300s TTL) & Refresh Token Rotation
- **Script / Command**: python 03_auth0_hardening_refresh_rotation.py / Auth0 Dashboard
- **Requirement Verification**: Auth0 Dashboard / terminal verification showing Token Expiration (TTL) reduced to 300 seconds (5 minutes) and Refresh Token Rotation ENABLED with 0s reuse grace interval.
- **Screenshot Placeholder**:
`	ext
[INSERT FULL SCREENSHOT 5 HERE]
`

---

### Screenshot 6: Old Refresh Token Replay Rejection
- **Title**: OAuth 2.0 Refresh Token Rotation Replay Attack Rejection
- **Script / Command**: python 03_auth0_hardening_refresh_rotation.py (Part 3)
- **Requirement Verification**: Terminal showing adversary attempting to replay an old invalidated refresh token (RT-1) after rotation, resulting in HTTP 400 Bad Request (invalid_grant: Access denied - Refresh token reuse detected).
- **Screenshot Placeholder**:
`	ext
[INSERT FULL SCREENSHOT 6 HERE]
`

---

### Screenshot 7: Real-Time Anomaly Detection Alert Firing
- **Title**: Real-Time AI Identity Anomaly Detection Engine (Volume Spike, Scope Jump, Expired Token)
- **Script / Command**: python 04_anomaly_detection.py
- **Requirement Verification**: Terminal showing real-time security anomaly alert firing with timestamp, identity, and event type (LLM_API_CALL_VOLUME_SPIKE, UNAUTHORIZED_SCOPE_CHANGE_DETECTED, EXPIRED_TOKEN_REUSE_ATTEMPT).
- **Screenshot Placeholder**:
`	ext
[INSERT FULL SCREENSHOT 7 HERE]
`

---

### Screenshot 8: Post-Hardening Attack Success Matrix & Comparison Table
- **Title**: Before vs After Defense Comparison Matrix & Overall Risk Reduction
- **Script / Command**: python 05_before_after_comparison.py
- **Requirement Verification**: Comprehensive comparison table showing Project 3 vs Project 4 outcomes across all 5 attacks with the specific control applied for each, demonstrating a 100.0% reduction in attack success rate.
- **Screenshot Placeholder**:
`	ext
[INSERT FULL SCREENSHOT 8 HERE]
`
