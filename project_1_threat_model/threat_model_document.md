# Project 1: AI Identity Security Threat Model — SecureNova Inc.

## 1. Executive Summary & Architecture Overview
SecureNova Inc. operates an AI-powered customer service platform comprising:
- **Human Users / Customers**: Interacting via Web / Mobile frontend.
- **Identity Provider (Auth0)**: Issues OAuth 2.0 / OIDC tokens with custom identity claims.
- **Autonomous AI Customer Service Agent (Agent A)**: Interprets user prompts, orchestrates tool use, and manages conversation state.
- **Internal Microservices & REST APIs**: CRM, Billing Engine, User Profile Service.
- **RAG Pipeline**: Vector Database (pgvector/Pinecone) containing enterprise documentation.
- **MCP Server Tools (Agent B / Gateway)**: Model Context Protocol server exposing tool capabilities.

```
[Human User] <--(OAuth 2.0 PKCE)--> [Auth0 IdP]
     |                                    |
(JWT Bearer)                         (Agent Claims)
     v                                    v
[AI Orchestrator Agent A] <--(mTLS / Ed25519)--> [MCP Server / Sub-Agent B]
     |                     |                                |
(Vector Query)       (M2M Token)                      (REST API)
     v                     v                                v
[RAG Vector DB]     [Internal REST API]             [Billing / DB System]
```

---

## 2. AI Identity Attack Surface Analysis
| Identity Entity | Identity Type | Auth Mechanism | Privileges / Scope | Associated Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Human User** | Human Identity | OAuth 2.0 PKCE + OIDC | `user:read`, `ticket:create` | Credential stuffing, session hijacking, prompt injection proxy |
| **AI Agent (Primary)** | Non-Human Identity (NHI) | Auth0 M2M Token + JWT | `agent:orchestrate`, `rag:read`, `mcp:call` | Indirect prompt injection, confused deputy, prompt extraction |
| **Sub-Agent / MCP Server** | Non-Human Identity (NHI) | Ed25519 Signed Envelope + JWT | `mcp:tools:execute`, `billing:write` | Agent identity spoofing, unauthorized tool execution |
| **OAuth Client App** | Service Identity | Client ID + Secret / PKCE | `openid profile email offline_access` | Token theft, authorization code interception |
| **Model API Key** | Secret Credential | Static Bearer Key | `llm:inference` | Secret hardcoding in system prompts, memory leakage |

---

## 3. STRIDE Threat Model for AI Identity Flows
| STRIDE Category | Target AI Boundary | Threat Description | Severity | Target OWASP / ATLAS |
| :--- | :--- | :--- | :--- | :--- |
| **Spoofing** | Agent-to-Agent / MCP Gateway | Attacker crafts a fake orchestrator JSON message to trick Agent B into privileged actions | **CRITICAL** | OWASP LLM09 / AML.T0054 |
| **Tampering** | RAG Vector Knowledge Base | Attacker poisons support knowledge chunks with prompt injection instructions | **HIGH** | OWASP LLM03 / AML.T0016 |
| **Repudiation** | MCP Tool Invocations | Non-human AI actions lack cryptographic non-repudiation or tamper-proof audit trails | **MEDIUM** | OWASP LLM08 / AML.T0040 |
| **Information Disclosure** | LLM Context to User Output | Indirect injection forces LLM to dump system prompt, internal API keys, or active JWTs | **CRITICAL** | OWASP LLM01, LLM07 / AML.T0051 |
| **Denial of Service** | LLM Inference API | Recursive tool calling or infinite reasoning loops triggered by malicious inputs | **MEDIUM** | OWASP LLM04 / AML.T0029 |
| **Elevation of Privilege** | User to MCP Privileged Tool | User manipulates agent role via prompt engineering to trigger billing refund tools | **HIGH** | OWASP LLM01 / AML.T0043 |

---

## 4. Trust Boundaries Breakdown
1. **Trust Boundary 1 (User -> AI Agent)**: Untrusted to Semi-Trusted. All text inputs, attachments, and headers must be treated as hostile.
2. **Trust Boundary 2 (AI Agent -> Auth0 IdP)**: Trusted. Standard OIDC / OAuth 2.0 PKCE flow with signed JWT verification.
3. **Trust Boundary 3 (AI Agent -> RAG Knowledge Base)**: Semi-Trusted to Trusted. Vector chunks can contain untrusted indirect injection payloads.
4. **Trust Boundary 4 (AI Agent -> MCP Server / Tool Gateway)**: Semi-Trusted. Requires cryptographic binding (Ed25519) and zero-trust validation.
5. **Trust Boundary 5 (AI Agent -> Model Provider)**: Trusted Transit / Egress. Must be protected against output credential leakage.

---

## 5. Threat Prioritization Matrix (DREAD Scoring)
| Threat ID | Threat Name | Damage | Reproducibility | Exploitability | Affected Users | Discoverability | DREAD Score | Risk Level |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **T-01** | Indirect Prompt Injection Credential Leak | 9 | 8 | 8 | 9 | 8 | **8.4 / 10** | **CRITICAL** |
| **T-02** | Inter-Agent Identity Spoofing (Agent B) | 9 | 8 | 7 | 8 | 7 | **7.8 / 10** | **HIGH** |
| **T-03** | System Prompt & System Role Extraction | 7 | 9 | 9 | 7 | 9 | **8.2 / 10** | **HIGH** |
| **T-04** | RAG Chunk Poisoning & MCP Tool Hijacking | 9 | 7 | 7 | 8 | 7 | **7.6 / 10** | **HIGH** |
| **T-05** | Replay of Stale M2M OAuth Credentials | 8 | 8 | 7 | 6 | 6 | **7.0 / 10** | **HIGH** |

---

## 6. Mitigation & Defensive Verification Architecture
- **Layer 1: Auth0 IAM & Custom Claims**: Inject `agent_id` and strict audience/scope verification on every request.
- **Layer 2: Short-Lived M2M Tokens & Rotation**: 300s TTL with automatic key rotation and replay rejection.
- **Layer 3: Cryptographic Binding**: Ed25519 asymmetric message signatures on all inter-agent messages.
- **Layer 4: Input / Output Guardrails**: Pre-LLM injection filter and Post-LLM regex redactor for sensitive patterns (JWT, API keys).
- **Layer 5: Continuous Zero-Trust Verification**: Enforce granular tool-level RBAC prior to any MCP tool execution.
