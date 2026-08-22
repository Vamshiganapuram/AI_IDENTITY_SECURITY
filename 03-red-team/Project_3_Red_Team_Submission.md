# Project 3: Red Team — AI Identity Attacks
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
