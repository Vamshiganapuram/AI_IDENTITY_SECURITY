# Project 4 — Blue Team: Guardrails, Hardening and Detection
**Organization**: SecureNova Inc.  
**Role**: AI Identity Security Engineer / Blue Team Specialist  
**Capstone Domain**: AI Identity Security, Zero-Trust Architecture & Threat Mitigation

---

## Overview & Objectives
This repository contains the complete defensive implementation for **Project 4: Blue Team Defense, Guardrails, Identity Hardening & Detection**.

The project fulfills all 5 core technical requirements and provides all evidence needed for the **8 required submission screenshots**:

1. **Input/Output Guardrails**: NeMo/Rebuff-style input filter blocking all 5 Project 3 attack payloads + Regex output credential redactor ([REDACTED]).
2. **Cryptographic Agent Identity Binding**: RFC 8032 Ed25519 asymmetric key generation (.pem files), inter-agent message signing, and tamper detection.
3. **Auth0 Hardening & Refresh Token Rotation**: Token TTL reduced to 300s, Refresh Token Rotation (RTR) enabled, and stale token replay rejection (400 Bad Request) + Custom Post-Login Risk Action (auth0_risk_engine_action.js).
4. **Real-Time Anomaly Detection Engine**: High-velocity call volume spike monitor (>20 req/60s), inter-agent scope escalation monitor, and expired token reuse monitor with structured telemetry.
5. **Before/After Defense Comparison Matrix**: Quantitative proof of 100% attack success reduction (from 100% exploit rate down to 0.0% residual risk).

---

## Repository Structure

`	ext
04-blue-team/
├── requirements.txt                         # Python dependencies (cryptography, PyJWT, colorama)
├── 01_input_output_guardrails.py            # [Screenshots 1 & 2] Input filter & Output JWT regex redactor
├── 02_crypto_identity_binding.py            # [Screenshots 3 & 4] Ed25519 key generation & tamper rejection
├── 03_auth0_hardening_refresh_rotation.py   # [Screenshots 5 & 6] Auth0 300s TTL & Refresh Token Rotation
├── 04_anomaly_detection.py                  # [Screenshot 7] Real-time AI Identity Anomaly Detectors
├── 05_before_after_comparison.py            # [Screenshot 8] Before/After Attack Comparison Matrix
├── auth0_risk_engine_action.js              # Production JavaScript Auth0 Post-Login Risk Action
├── run_all_blue_team.py                     # Master runner executing all verification suites
├── agent_ed25519_private.pem                # Generated Ed25519 Private Key
├── agent_ed25519_public.pem                 # Generated Ed25519 Public Key
└── Project_4_Blue_Team_Submission_Guide.md  # Detailed step-by-step submission guide
`

---

## Quick Start & Execution

### 1. Install Dependencies
`ash
pip install -r requirements.txt
`

### 2. Run Individual Modules (To Capture Specific Screenshots)
`ash
# Step 1: Screenshots 1 & 2 (Input Guardrails & Output Redaction)
python 01_input_output_guardrails.py

# Step 2: Screenshots 3 & 4 (Ed25519 Key Generation & Tamper Rejection)
python 02_crypto_identity_binding.py

# Step 3: Screenshots 5 & 6 (Auth0 Dashboard Settings & Token Replay Rejection)
python 03_auth0_hardening_refresh_rotation.py

# Step 4: Screenshot 7 (Real-time Anomaly Detection Alerts)
python 04_anomaly_detection.py

# Step 5: Screenshot 8 (Before vs After Comparison Matrix)
python 05_before_after_comparison.py
`

### 3. Run All Modules Sequentially
`ash
python run_all_blue_team.py
`
