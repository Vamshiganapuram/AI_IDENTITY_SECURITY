# Project 1: Threat Model — AI Identity Security
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
