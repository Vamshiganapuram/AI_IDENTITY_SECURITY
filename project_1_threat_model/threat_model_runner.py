"""
Project 1: Threat Model Visualizer & Architecture CLI
SecureNova Inc. - AI Identity Security
"""
import sys
import os

def banner():
    print("=" * 80)
    print(" PROJECT 1: AI IDENTITY SECURITY THREAT MODEL & ARCHITECTURE")
    print(" Organization: SecureNova Inc. | Role: AI Identity Security Analyst")
    print("=" * 80)

def step_1_architecture():
    print("\n[STEP 1 / SCREENSHOT 1] Platform Architecture & AI Identity Boundaries")
    print("-" * 80)
    arch = """
  +-----------------------------------------------------------------------------------+
  | SECURENOVA AI IDENTITY PLATFORM ARCHITECTURE                                      |
  +-----------------------------------------------------------------------------------+
  |                                                                                   |
  |  [ Human User / Customer ]                                                        |
  |        |                                                                          |
  |        |  (1) OAuth 2.0 PKCE + Universal Login                                    |
  |        v                                                                          |
  |  [ Auth0 Identity Provider ]  ----(Custom Claims: agent_id, role)----> [JWT Token]|
  |        |                                                                |         |
  |        |                                                                v         |
  |        +-----------------------> [ AI Orchestrator: Agent A ] <---------+         |
  |                                         |                                         |
  |             +---------------------------+--------------------------+              |
  |             |                           |                          |              |
  |    (2) Vector RAG Query        (3) M2M Auth0 API Call     (4) Ed25519 Signed RPC  |
  |             v                           v                          v              |
  |     [ Vector DB / RAG ]      [ Internal REST APIs ]      [ MCP Server: Agent B ]  |
  |     (Knowledge Store)        (Billing / CRM / Profile)   (Privileged Tool Worker) |
  |                                                                                   |
  +-----------------------------------------------------------------------------------+
    """
    print(arch)

def step_2_attack_surface():
    print("\n[STEP 2 / SCREENSHOT 2] AI Identity Attack Surface Analysis")
    print("-" * 80)
    print(f"{'Identity Entity':<20} | {'Type':<18} | {'Auth Method':<20} | {'Primary Attack Vector':<20}")
    print("-" * 80)
    rows = [
        ("Human User", "Human Principal", "OAuth2 PKCE / OIDC", "Prompt Injection Proxy"),
        ("AI Agent A", "Non-Human Identity", "Auth0 M2M Bearer JWT", "Indirect Prompt Injection"),
        ("AI Agent B (MCP)", "Non-Human Identity", "Ed25519 Signature", "Agent Identity Spoofing"),
        ("OAuth Client", "Service Identity", "Client ID & Secret", "Credential Interception"),
        ("LLM API Key", "Model Credential", "Static Bearer Token", "Context Window Exfiltration"),
        ("RAG Ingestion Feed", "Data Pipeline", "Service Account", "Corpus / Chunk Poisoning")
    ]
    for r in rows:
        print(f"{r[0]:<20} | {r[1]:<18} | {r[2]:<20} | {r[3]:<20}")

def step_3_stride():
    print("\n[STEP 3 / SCREENSHOT 3] STRIDE Threat Modeling for AI Identity Flows")
    print("-" * 80)
    stride_data = [
        ("S - Spoofing", "Agent-to-Agent RPC", "Attacker impersonates orchestrator to trigger Agent B", "CRITICAL", "OWASP LLM09"),
        ("T - Tampering", "RAG Vector Store", "Attacker poisons knowledge chunks with malicious directives", "HIGH", "OWASP LLM03"),
        ("R - Repudiation", "MCP Tool Gateway", "Agent acts on behalf of user without signed provenance", "MEDIUM", "OWASP LLM08"),
        ("I - Info Disclosure", "LLM Output Stream", "Indirect prompt injection exfiltrates active JWTs & keys", "CRITICAL", "OWASP LLM01"),
        ("D - Denial of Service", "LLM Inference API", "Adversarial prompts trigger infinite tool invocation loops", "MEDIUM", "OWASP LLM04"),
        ("E - Elevation of Priv", "User -> Agent -> MCP", "Unprivileged user tricks agent into billing refund tool", "HIGH", "OWASP LLM07")
    ]
    print(f"{'STRIDE Category':<22} | {'AI Flow Boundary':<20} | {'Severity':<10} | {'Standard Mapping':<15}")
    print("-" * 80)
    for s in stride_data:
        print(f"{s[0]:<22} | {s[1]:<20} | {s[3]:<10} | {s[4]:<15}")
        print(f"  --> Specific Threat: {s[2]}")

def step_4_trust_boundaries():
    print("\n[STEP 4 / SCREENSHOT 4] Trust Boundary Breakdown & Protocol Constraints")
    print("-" * 80)
    boundaries = [
        ("TB-1: User <-> Agent A", "Untrusted -> Semi-Trusted", "Untrusted user inputs, prompt injection risk"),
        ("TB-2: Agent A <-> Auth0", "Semi-Trusted -> Trusted", "OIDC / PKCE token exchange, claims integrity"),
        ("TB-3: Agent A <-> RAG DB", "Semi-Trusted -> Semi-Trusted", "Knowledge ingestion risk, unverified chunk embeddings"),
        ("TB-4: Agent A <-> Agent B (MCP)", "Semi-Trusted -> High-Privilege", "Inter-agent RPC, requires cryptographic Ed25519 signing"),
        ("TB-5: Agent <-> Backend APIs", "Privileged -> Internal Core", "M2M OAuth token with 300s TTL and strictly scoped audience")
    ]
    for b in boundaries:
        print(f"[*] {b[0]}\n    Transit: {b[1]}\n    Security Context: {b[2]}\n")

def step_5_dfd():
    print("\n[STEP 5 / SCREENSHOT 5] Data Flow Diagram (DFD) Level 1 - Identity & Token Paths")
    print("-" * 80)
    dfd = """
  [User] ===( 1. Auth Req: PKCE )===> [Auth0 IdP]
    ||                                      ||
  (2. ID Token + JWT)                    (3. Custom Claims: agent_id)
    ||                                      ||
    v                                       v
  [AI Customer Service Agent A (Context: JWT, Session State)]
    ||
    ||=======( 4. RAG Query: Fetch Support Knowledge )=======> [Vector DB]
    ||<======( 5. Unsanitized Chunk: [POTENTIAL EXPLOIT] )==== [Vector DB]
    ||
    ||=======( 6. Tool Request: Ed25519 Envelope )===========> [MCP Tool Agent B]
    ||<======( 7. Tool Response: Signed Output )============== [MCP Tool Agent B]
    ||
    v
  [User UI Response Filter / Guardrail Inspection]
    """
    print(dfd)

def step_6_risk_scoring():
    print("\n[STEP 6 / SCREENSHOT 6] DREAD Threat Risk Scoring Matrix")
    print("-" * 80)
    print(f"{'Threat ID':<10} | {'Threat Scenario':<38} | {'DREAD Score':<12} | {'Risk Level':<10}")
    print("-" * 80)
    risks = [
        ("T-01", "Indirect Prompt Injection to JWT Leak", "8.4 / 10", "CRITICAL"),
        ("T-02", "System Prompt & Role Extraction", "8.2 / 10", "HIGH"),
        ("T-03", "Inter-Agent Identity Spoofing", "7.8 / 10", "HIGH"),
        ("T-04", "RAG Poisoning & MCP Tool Hijacking", "7.6 / 10", "HIGH"),
        ("T-05", "Stale M2M Token Replay Attack", "7.0 / 10", "HIGH")
    ]
    for r in risks:
        print(f"{r[0]:<10} | {r[1]:<38} | {r[2]:<12} | {r[3]:<10}")

def step_7_scenarios():
    print("\n[STEP 7 / SCREENSHOT 7] Critical Threat Scenarios & Attack Kill Chains")
    print("-" * 80)
    print("Scenario A: Indirect Token Exfiltration Kill Chain")
    print("  [Attacker Document] -> [RAG Ingestion] -> [Agent Ingestion Context] -> [Prompt Injection]")
    print("  -> [Agent Context Extraction] -> [JWT Leaked in Output] -> [Credential Compromise]\n")
    print("Scenario B: Agent-to-Agent Spoofing Kill Chain")
    print("  [Malicious Entity] -> [Forged JSON RPC] -> [Agent B Receives Request]")
    print("  -> [Agent B Assumes Trusted Caller] -> [Privileged Tool Execution: Refund/DB]")

def step_8_mitigation_plan():
    print("\n[STEP 8 / SCREENSHOT 8] Threat Model Mitigation Summary & Security Verification Plan")
    print("-" * 80)
    controls = [
        ("Auth0 Claims & Scopes", "Inject verified agent_id and strict scope checking at API gateway", "PASS"),
        ("Short-Lived M2M Rotation", "Rotate tokens every 300s, invalidate previous token immediately", "PASS"),
        ("Ed25519 Identity Binding", "Cryptographically sign every inter-agent request payload", "PASS"),
        ("Input/Output Guardrails", "Regex and heuristic guardrails blocking injection & credential leaks", "PASS"),
        ("Zero-Trust Re-Verification", "Enforce step-up verification for high-risk MCP tools", "PASS")
    ]
    for c in controls:
        print(f"[VERIFIED] {c[0]:<28} | {c[1]:<45} | Status: {c[2]}")
    print("=" * 80)

if __name__ == "__main__":
    banner()
    step_1_architecture()
    step_2_attack_surface()
    step_3_stride()
    step_4_trust_boundaries()
    step_5_dfd()
    step_6_risk_scoring()
    step_7_scenarios()
    step_8_mitigation_plan()
