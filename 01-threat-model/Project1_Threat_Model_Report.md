# Project 1 — Threat Model the AI Identity System

**Course:** AI Identity Security Capstone  
**Organization:** SecureNova Inc.  
**Role:** AI Identity Security Analyst  
**System:** LLM-powered customer service using Auth0, a RAG pipeline, MCP tool servers, and internal REST APIs

## 1. Threat modelling — identity inventory

SecureNova’s platform has **human and non-human identities**. For each type, authentication and privilege are explicit. There is no implicit trust between the user layer, the agent layer, and the internal API layer.

| Identity type | Authentication mechanism | Privilege level |
|---------------|--------------------------|-----------------|
| Human user (customer) | Auth0 Universal Login; OAuth 2.0 Authorization Code + **PKCE**; **OIDC** ID token | Own profile, own tickets, own chat session. No API-key or M2M secret access. |
| Human user (CSR / supervisor) | Same + **MFA**; Enterprise Connection SSO | Assigned queue; no LLM provider keys; no Auth0 tenant admin. |
| Human user (security admin) | OIDC + MFA + Auth0 dashboard RBAC | Tenant attack-protection config and audit review. No standing production LLM keys in the browser. |
| AI agent (customer-service orchestrator) | **On-Behalf-Of** user access token + confidential **M2M** client credentials (short-lived JWT) | Delegated user scopes **plus** constrained tool scopes. Cannot mint admin tokens. |
| OAuth M2M client | Client Credentials grant against Auth0; JWT `aud` bound to internal APIs | `tickets:read`, `tickets:write`, `kb:search` only. Separate client for admin jobs. |
| LLM API key (model service account) | Provider secret from a vault; **rotated** (hourly/daily) | Inference only. Never placed in prompts, RAG chunks, or MCP responses. |
| RAG pipeline service identity | Workload identity / M2M JWT to the vector database | Read for retrieve; **separate** identity for ingest/write. |
| MCP server identity | OAuth resource server + mTLS; optional **Ed25519** invocation signatures | Execute **allow-listed** tools only; re-verify every agent-to-agent call (Zero Trust). |

### Trust boundaries

1. **User Layer** — browsers, Universal Login, social and enterprise IdPs, public chat channel.
2. **Agent Layer** — orchestrator, secret checkout, prompt assembly, LLM calls.
3. **Internal API Layer** — REST resource servers, RAG/vector DB, MCP tools, audit store.

STRIDE is applied on every identity flow that **crosses** these boundaries.

## 2. STRIDE matrix and Threat Dragon DFD

Import `deliverables/SecureNova_AI_Identity_ThreatDragon.json` into OWASP Threat Dragon.

The **AI Agent Orchestrator** process carries all six STRIDE categories (use that process for the threat-panel screenshot). The full flow-by-flow matrix is `deliverables/STRIDE_Threat_Matrix.csv` and `deliverables/STRIDE_Matrix_and_Risk_Register.html`.

## 3. Attack trees (draw.io) and scoring

**Risk Score = Likelihood × Impact** (each on a 1–5 scale).

| Tree | Goal | Highest-likelihood path (summary) | L | I | Score | Closest ATLAS ID |
|------|------|-----------------------------------|---|---|-------|------------------|
| 1 | LLM API key exfiltration via prompt injection | Direct or indirect injection while secrets exist in runtime context | 5 | 5 | **25** | **AML.T0051** |
| 2 | Agent identity spoofing → elevated API scope | Stolen OBO/M2M material plus an over-broad M2M client | 4 | 5 | **20** | **AML.T0073** |
| 3 | RAG chunk poisoning | Ingest write path plus unsigned chunks | 4 | 4 | **16** | **AML.T0070** |

Supporting techniques: **AML.T0083** (credentials from agent configuration), **AML.T0055** (unsecured credentials), **AML.T0012** (valid accounts), **AML.T0051.001** (indirect prompt injection).

## 4. MITRE ATLAS mapping

| Attack path | Closest technique | URL |
|-------------|-------------------|-----|
| Prompt injection → key leak | AML.T0051 LLM Prompt Injection | https://atlas.mitre.org/techniques/AML.T0051 |
| Spoof agent / abuse tokens | AML.T0073 Impersonation | https://atlas.mitre.org/techniques/AML.T0073 |
| Poison retrieval corpus | AML.T0070 RAG Poisoning | https://atlas.mitre.org/techniques/AML.T0070 |

Screenshot **AML.T0051** for the required ATLAS evidence (primary technique on Attack Tree 1).

## 5. Risk-ranked register with owners

| Rank | ID | Score | Threat | Owner |
|------|----|-------|--------|-------|
| 1 | R-01 | 25 | LLM API key exfiltration via prompt injection | AI Platform / Secrets Owner |
| 2 | R-02 | 20 | Agent identity spoofing to elevated API scope | IAM / Auth0 Administrator |
| 3 | R-04 | 20 | Indirect prompt injection from tickets into RAG | Agent Runtime Owner |
| 4 | R-06 | 20 | M2M client secret in prompt or repository | Secrets Owner |
| 5 | R-03 | 16 | RAG chunk poisoning manipulating agent tools | Knowledge Engineering Lead |
| 6 | R-08 | 16 | Auth0 brute force / credential stuffing on Universal Login | Auth0 Administrator |
| 7 | R-12 | 16 | PII leakage from API responses into model logs | Privacy + AI Platform |
| 8 | R-05 | 15 | MCP tool spoofing / unauthorized tool invocation | MCP Platform Owner |
| 9 | R-07 | 12 | Missing audit for non-human identities | SOC / Detection Engineering |
| 10 | R-10 | 12 | Recursive MCP/tool loop denial of service | SRE / AI Platform |
| 11 | R-11 | 10 | Enterprise SSO group-to-role mis-mapping | IAM / Auth0 Administrator |
| 12 | R-09 | 9 | System prompt / policy extraction | Agent Runtime Owner |

Full columns (STRIDE, ATLAS, OWASP LLM, treatment) are in `deliverables/Risk_Register.csv`.

## 6. Notes for the wider capstone concept list

Project 1 already documents: AI identity attack surface; STRIDE on identity flows and trust boundaries; OAuth 2.0 + PKCE and OIDC via Auth0; federated SSO; short-lived M2M and LLM keys; prompt injection (OWASP LLM01, LLM07); agent spoofing and RAG poisoning (LLM09 / supply chain); Zero Trust (no implicit agent trust); OWASP LLM mapping; Auth0 attack protection as a control on the login flow; monitoring via the identity audit-log flow.

Guardrails, cryptographic binding details, NIST AI RMF policy text, and a live red-team campaign belong in later projects — they are not extra screenshot types for Project 1.
