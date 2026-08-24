# SecureNova AI Identity Security — Capstone Project

Complete implementation, threat modeling, IAM configuration, Red Team exploitation suite, Blue Team guardrails, and compliance governance for the **SecureNova AI-Powered Customer Service Platform**.

---

## Repository Structure & Folder Layout

```
ai-identity-security-capstone/
├── config.py                               # Central platform configuration and secrets
├── requirements.txt                        # Python dependencies
├── run_full_capstone.py                    # Master script to run entire project end-to-end
├── generate_submission_docs.py             # Generates submission document templates
│
├── project_1_threat_model/                 # PROJECT 1: Threat Model (8 Screenshots)
│   ├── threat_model_document.md            # Comprehensive STRIDE Threat Model & DFDs
│   └── threat_model_runner.py              # Visualizer CLI for architecture, attack surface, DFD
│
├── project_2_iam_auth0/                    # PROJECT 2: IAM & Identity Controls (8 Screenshots)
│   ├── auth0_action_post_login.js          # Auth0 Post-Login Action injecting custom claims
│   ├── oauth_agent_client.py               # OAuth 2.0 PKCE client & JWT token inspector
│   ├── sso_client_simulator.py             # Multi-client Federated SSO demonstration
│   ├── auth0_attack_protection_audit.py    # Auth0 Attack Protection security configs
│   └── credential_rotation_m2m.py          # Short-lived M2M token rotation & 401 replay defense
│
├── project_3_red_team/                     # PROJECT 3: Red Team Attacks (8 Screenshots)
│   ├── red_team_runner.py                  # Executes 5 identity attack vectors & CVSS matrix
│   └── cvss_atlas_report.md                # CVSS 3.1 vectors, MITRE ATLAS mappings & findings
│
├── project_4_blue_team/                    # PROJECT 4: Blue Team Defense (8 Screenshots)
│   ├── guardrails_engine.py                # Input/output guardrails & Ed25519 signing engine
│   └── blue_team_runner.py                 # Runs defense suite, proving 0% residual exploit rate
│
└── project_5_governance_compliance/        # Governance & Enterprise Compliance
    └── ai_identity_governance_policy.md    # NIST AI RMF 1.0 & OWASP Top 10 Policy & Playbook
```

---

## Quick Start & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Individual Projects
- **Project 1 (Threat Model)**:
  ```bash
  python project_1_threat_model/threat_model_runner.py
  ```
- **Project 2 (IAM & Auth0 Controls)**:
  ```bash
  python project_2_iam_auth0/oauth_agent_client.py
  python project_2_iam_auth0/sso_client_simulator.py
  python project_2_iam_auth0/auth0_attack_protection_audit.py
  python project_2_iam_auth0/credential_rotation_m2m.py
  ```
- **Project 3 (Red Team Exploits)**:
  ```bash
  python project_3_red_team/red_team_runner.py
  ```
- **Project 4 (Blue Team Guardrails)**:
  ```bash
  python project_4_blue_team/blue_team_runner.py
  ```

### 3. Run Entire Suite in One Command
```bash
python run_full_capstone.py
```
