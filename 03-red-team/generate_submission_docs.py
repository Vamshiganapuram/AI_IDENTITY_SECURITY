"""
Submission Document Template Generator
Generates ready-to-use Word/Markdown documentation templates for all 4 projects with exact screenshot titles and descriptions.
"""
import os

DOCS = {
    "Project_1_Threat_Model_Submission.md": """# Project 1: Threat Model — AI Identity Security
**Company / Organization**: SecureNova Inc.  
**Role**: AI Identity Security Analyst  
**Submission**: Project 1 (8 Screenshots)

---

### Screenshot 1: AI Platform Architecture & Identity Trust Boundaries
- **Description**: Full architectural diagram of SecureNova customer service platform showing Human Users, Auth0 IdP, Orchestrator Agent A, RAG Vector DB, Internal REST APIs, and MCP Tool Server B.
- **Image**: `[INSERT SCREENSHOT 1 HERE]`

---

### Screenshot 2: AI Identity Attack Surface Analysis
- **Description**: Attack surface breakdown covering Human Users, Non-Human Identities (Agent A & B), OAuth Clients, API Keys, and RAG Ingestion pipelines with respective attack vectors.
- **Image**: `[INSERT SCREENSHOT 2 HERE]`

---

### Screenshot 3: STRIDE Threat Modeling Matrix
- **Description**: Comprehensive STRIDE threat categorization mapping Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege across AI boundaries.
- **Image**: `[INSERT SCREENSHOT 3 HERE]`

---

### Screenshot 4: Trust Boundary Breakdown & Security Constraints
- **Description**: Detailed protocol analysis of Trust Boundaries TB-1 through TB-5, defining trust transitions and required security mechanisms (OAuth PKCE, Ed25519 signatures, M2M tokens).
- **Image**: `[INSERT SCREENSHOT 4 HERE]`

---

### Screenshot 5: Data Flow Diagram (DFD) Level 1 with Token Paths
- **Description**: Data Flow Diagram showing user authentication flow, Auth0 custom claim token issuance, vector query flow, and signed MCP tool execution paths.
- **Image**: `[INSERT SCREENSHOT 5 HERE]`

---

### Screenshot 6: DREAD Risk Scoring & Threat Prioritization
- **Description**: Risk scoring table prioritizing the top 5 AI identity threats based on Damage, Reproducibility, Exploitability, Affected Users, and Discoverability.
- **Image**: `[INSERT SCREENSHOT 6 HERE]`

---

### Screenshot 7: Attack Scenarios & Multi-Step Kill Chains
- **Description**: Step-by-step kill chains for Indirect Prompt Injection Credential Leak and Inter-Agent Identity Spoofing.
- **Image**: `[INSERT SCREENSHOT 7 HERE]`

---

### Screenshot 8: Mitigation Summary & Security Verification Plan
- **Description**: Comprehensive mitigation table outlining implemented controls and verification status across all AI identity layers.
- **Image**: `[INSERT SCREENSHOT 8 HERE]`
""",

    "Project_2_IAM_Auth0_Submission.md": """# Project 2: IAM & Identity Controls with Auth0
**Company / Organization**: SecureNova Inc.  
**Role**: AI Identity Security Analyst  
**Submission**: Project 2 (8 Screenshots)

---

### Screenshot 1: Auth0 Application Settings Dashboard
- **Description**: Auth0 Management Dashboard showing the registered AI Agent application (`SecureNova-Customer-Agent`), Client ID, Allowed Callback URLs, and PKCE grant configuration.
- **Image**: `[INSERT SCREENSHOT 1 HERE]`

---

### Screenshot 2: OAuth 2.0 + PKCE Authorization Flow
- **Description**: Authorization request URL and terminal/browser execution displaying `code_challenge`, `code_verifier`, and `state` parameters conforming to RFC 7636.
- **Image**: `[INSERT SCREENSHOT 2 HERE]`

---

### Screenshot 3: Auth0 Post-Login Action Code
- **Description**: JavaScript implementation of Auth0 post-login Action injecting non-human identity claims (`https://securenova.ai/agent_id`, `trust_tier`, `allowed_tools`) into the ID/Access tokens.
- **Image**: `[INSERT SCREENSHOT 3 HERE]`

---

### Screenshot 4: JWT Token Inspection & Custom Claims at jwt.io
- **Description**: Decoded JWT token on jwt.io / terminal inspector confirming the presence of verified claims (`agent_id`, `roles`, `tenant_id`, `sub`) and valid cryptographic signature.
- **Image**: `[INSERT SCREENSHOT 4 HERE]`

---

### Screenshot 5: Federated Single Sign-On (SSO) Demonstration
- **Description**: Multi-client SSO validation showing a user authenticated to Client 1 (Customer Service Agent) automatically granted access to Client 2 (Analytics Agent) via IdP session cookies without re-authenticating.
- **Image**: `[INSERT SCREENSHOT 5 HERE]`

---

### Screenshot 6: Auth0 Attack Protection Dashboard
- **Description**: Tenant security configuration showing Brute-Force Protection, Suspicious IP Throttling, Breached Password Detection, and Adaptive MFA enabled.
- **Image**: `[INSERT SCREENSHOT 6 HERE]`

---

### Screenshot 7: Short-Lived M2M Token Issuance
- **Description**: Machine-to-Machine OAuth Client Credentials grant issuing a short-lived bearer token (TTL = 300s) for Agent-to-REST API communication.
- **Image**: `[INSERT SCREENSHOT 7 HERE]`

---

### Screenshot 8: Credential Rotation Script (200 OK then 401 Unauthorized Replay)
- **Description**: Terminal execution of credential rotation engine showing initial authorized call returning timestamped `200 OK`, followed by an automated secret rotation and subsequent replay rejection returning timestamped `401 Unauthorized`.
- **Image**: `[INSERT SCREENSHOT 8 HERE]`
""",

    "Project_3_Red_Team_Submission.md": """# Project 3: Red Team — AI Identity Attacks
**Company / Organization**: SecureNova Inc.  
**Role**: AI Red Team Security Analyst  
**Submission**: Project 3 (8 Screenshots)

---

### Screenshot 1: Indirect Prompt Injection — JWT Credential Exfiltration
- **Description**: Agent terminal output showing simulated JWT session token leaked in the model response after ingesting an adversarial document containing an injection payload (OWASP LLM01).
- **Image**: `[INSERT SCREENSHOT 1 HERE]`

---

### Screenshot 2: Inter-Agent Identity Spoofing & Unauthorized Tool Execution
- **Description**: Two-agent terminal output showing Agent B executing a privileged action (`issue_billing_refund`) after receiving an unauthenticated spoofed JSON message pretending to originate from the Orchestrator (OWASP LLM09).
- **Image**: `[INSERT SCREENSHOT 2 HERE]`

---

### Screenshot 3: System Prompt Extraction & Role Elevation
- **Description**: Model output displaying partial/full system prompt content extracted via prompt engineering techniques (Repeat-Back, Role-Play, Translation) and unauthorized elevation to Admin role (OWASP LLM07).
- **Image**: `[INSERT SCREENSHOT 3 HERE]`

---

### Screenshot 4: RAG Chunk Poisoning & MCP Tool Hijacking
- **Description**: Terminal output showing agent retrieving a poisoned knowledge base chunk from vector storage and autonomously executing an unauthorized MCP tool call on behalf of the attacker.
- **Image**: `[INSERT SCREENSHOT 4 HERE]`

---

### Screenshot 5: CVSS 3.1 Calculator at first.org
- **Description**: Complete CVSS 3.1 calculator screenshot at first.org for the highest-severity finding (Inter-Agent Spoofing: Score **9.9 CRITICAL**), with all Base Score metric vector components selected.
- **Image**: `[INSERT SCREENSHOT 5 HERE]`

---

### Screenshot 6: MITRE ATLAS Technique Page (AML.T0051 / AML.T0054)
- **Description**: MITRE ATLAS website showing the technique reference page for mapped AI identity vulnerabilities (e.g., AML.T0051 LLM Prompt Injection or AML.T0054 LLM Agent Hijacking).
- **Image**: `[INSERT SCREENSHOT 6 HERE]`

---

### Screenshot 7: CVSS 3.1 Findings & Scoring Table
- **Description**: Structured table scoring all 5 Red Team attack findings with their respective CVSS 3.1 vector strings, base scores, and severities.
- **Image**: `[INSERT SCREENSHOT 7 HERE]`

---

### Screenshot 8: Baseline Attack Success Matrix (Pre-Defense)
- **Description**: Attack success matrix showing 100% success rate across all 5 evaluated attack categories prior to the deployment of defensive guardrails.
- **Image**: `[INSERT SCREENSHOT 8 HERE]`
""",

    "Project_4_Blue_Team_Submission.md": """# Project 4: Blue Team — Guardrails, Hardening & Detection
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
"""
}

def generate_templates():
    out_dir = os.path.dirname(__file__)
    for filename, content in DOCS.items():
        filepath = os.path.join(out_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] Generated submission document template: {filename}")

if __name__ == "__main__":
    generate_templates()
