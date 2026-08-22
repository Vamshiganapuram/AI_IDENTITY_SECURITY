# Project 2: IAM & Identity Controls with Auth0
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
