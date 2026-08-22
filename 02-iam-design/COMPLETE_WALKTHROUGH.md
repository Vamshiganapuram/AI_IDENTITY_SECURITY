# COMPLETE WALKTHROUGH — AI Identity Security capstone

Read this file from top to bottom. Do not skip. Nothing is assumed except:

- You created a **GitHub repository** whose folder is this project (name can be `project2-auth0-ai-app`).
- You can install programs on this Windows PC.

Mettl wants **full-screen** screenshots, **address bar or terminal title visible**, one Word file per project, then PDF, then one ZIP.

---

# Part A — Put the files into GitHub (do this first)

These files were created on disk in:

`C:\Users\asus\Documents\project2-auth0-ai-app`

## A1. If GitHub Desktop / website repo is empty

1. Open GitHub in the browser and open your new repository.
2. If you have **not** cloned it yet, in PowerShell:

```text
cd $HOME\Documents
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME`.

3. If the clone is empty (only README / LICENSE), **copy everything** from `C:\Users\asus\Documents\project2-auth0-ai-app` into the clone folder. Overwrite README if asked.

Include all of these (do not pick only some):

```text
app.py
requirements.txt
.env.example
.gitignore
auth0\post_login_action.js
scripts\credential_rotation.py
scripts\run_red_team.py
scripts\run_blue_team.py
static\index.html
static\app.js
static\styles.css
static\lab.html
static\lab.js
lab\   (entire folder)
01-threat-model\   (entire folder)
03-red-team\   (entire folder)
05-governance\   (entire folder)
COMPLETE_WALKTHROUGH.md
START_HERE.md
AUTH0_SETUP.md
SCREENSHOT_PLAYBOOK.md
README.md
```

4. Open PowerShell **in the clone folder** (the folder that contains `app.py`):

```text
cd path\to\YOUR_REPO_NAME
git add .
git status
```

Confirm `.env` is **not** listed. If `.env` is listed, stop — `.gitignore` must contain a line that is exactly `.env`.

5. Commit and push (only if you want GitHub backup; **never push secrets**):

```text
git commit -m "Add SecureNova AI identity capstone lab"
git push
```

You do **not** import this GitHub repo into Auth0. Auth0 is configured in the browser. GitHub only stores the lab code.

## A2. Files you create later on this PC only (never GitHub)

| File / folder | When |
|---------------|------|
| `.env` | After Auth0 apps exist |
| `.venv\` | Python creates this |
| `lab\keys\` | Created automatically on first blue-team run |

---

# Part B — Install software (once)

## B1. Python

1. Open https://www.python.org/downloads/
2. Download Python 3.12 or 3.13.
3. Run installer. Tick **Add python.exe to PATH**.
4. Install Now. Finish.
5. Close any old PowerShell windows. Open a **new** PowerShell:

```text
python --version
pip --version
```

You must see version numbers.

## B2. Git (if `git` is not found)

Install from https://git-scm.com/download/win then open a new PowerShell.

## B3. Other accounts / apps

- Chrome or Edge
- Microsoft Word
- Phone: Google Authenticator or Microsoft Authenticator
- Free Auth0 account (created in Project 2)
- Optional: GitHub account (already done)

---

# Part C — Project 1 — Threat model (8 screenshots)

You do **not** run Python for Project 1.

## C1. Threat Dragon DFD — SCREENSHOT P1-1

1. Open folder `01-threat-model\deliverables\`
2. Browser: https://www.threatdragon.com
3. Use **local / device** (avoid GitHub login if it blocks you).
4. Open / import `SecureNova_AI_Identity_ThreatDragon.json`
5. Confirm three trust boundaries: **User Layer**, **Agent Layer**, **Internal API Layer**.
6. **SCREENSHOT P1-1:** full screen, URL bar, entire data-flow diagram visible.

## C2. STRIDE panel — SCREENSHOT P1-2

1. Click the process named **AI Agent Orchestrator**.
2. Open its threats so you see at least Spoofing, Information Disclosure, Elevation of Privilege.
3. **SCREENSHOT P1-2:** full screen, URL, threat panel visible.

If the JSON will not import, draw the same labeled DFD by hand in Threat Dragon (same names) and add those threats on the orchestrator.

## C3–C5. Attack trees in draw.io

1. Open https://app.diagrams.net
2. **Open Existing Diagram** → Device → choose the file.
3. Zoom so **every node** is visible, including the ATLAS box at the bottom.
4. URL must show `app.diagrams.net`.

| Shot | File |
|------|------|
| **SCREENSHOT P1-3** | `AttackTree1_LLM_API_Key_Exfiltration.drawio` |
| **SCREENSHOT P1-4** | `AttackTree2_Agent_Identity_Spoofing.drawio` |
| **SCREENSHOT P1-5** | `AttackTree3_RAG_Chunk_Poisoning.drawio` |

## C6–C7. STRIDE matrix and risk register

1. Double-click `01-threat-model\deliverables\STRIDE_Matrix_and_Risk_Register.html`
   (or File → Open with Chrome).
2. **SCREENSHOT P1-6:** the STRIDE matrix table (full window; if the path is `file:///...` that is OK, keep it visible).
3. Scroll to **Risk Register** (10+ scored rows).
4. **SCREENSHOT P1-7:** risk register.

## C8. MITRE ATLAS

1. Open https://atlas.mitre.org/techniques/AML.T0051
2. **SCREENSHOT P1-8:** full page, URL visible.

Also keep these URLs for the report (no extra required shots):

- https://atlas.mitre.org/techniques/AML.T0073
- https://atlas.mitre.org/techniques/AML.T0070

## C9. Word → PDF for Project 1

1. Word → new document → title `Project 1 — Threat Model`
2. Paste shots **P1-1 … P1-8** in that order. Type a heading above each image.
3. File → Save As → PDF: `Project1_Threat_Model.pdf`
4. Put the PDF aside for the final ZIP.

Read `01-threat-model\Project1_Threat_Model_Report.md` if the examiner wants a written report in the same PDF (paste the text above the screenshots or after them).

---

# Part D — Project 2 — Auth0 IAM (8 screenshots)

The **only file you paste into Auth0** is `auth0\post_login_action.js`.  
Nothing else from GitHub is imported into Auth0.

## D0. Create tenant

1. https://auth0.com → Sign up.
2. Create tenant (example name `securenova-ai`), region closest to you, **Development**.
3. Write the domain in Notepad, like `securenova-ai.us.auth0.com` (no `https://`).

## D1. API + scopes — SCREENSHOT P2-2 (take after permissions exist)

1. **Applications → APIs → + Create API**
2. Name: `SecureNova AI API`
3. Identifier: `https://securenova-ai-api` (copy exactly)
4. Signing: RS256 → Create
5. **Permissions** tab — add:
   - `read:ai-data` — User-level AI chat data
   - `write:admin` — Admin-level operations
6. **Settings** tab:
   - Token Expiration (Seconds): `60`
   - Enable RBAC: ON
   - Add Permissions in the Access Token: ON
   - Save
7. **SCREENSHOT P2-2:** Permissions tab with **both** scopes visible. Full screen + URL.

## D2. App 1 — browser chat (PKCE)

1. **Applications → Applications → + Create Application**
2. Name: `SecureNova AI Chat`
3. Type: **Regular Web Applications** → Create
4. Settings → **Application Type** → change to **Single Page Application**  
   If it will not change: create a new app with type **Single Page Application** and use that as the chat app.
5. Application URIs (exact):

| Field | Value |
|--------|--------|
| Allowed Callback URLs | `http://localhost:8000/` |
| Allowed Logout URLs | `http://localhost:8000/` |
| Allowed Web Origins | `http://localhost:8000` |
| Allowed Origins (CORS) | `http://localhost:8000` |

6. Advanced Settings → Grant Types: Authorization Code, Refresh Token. Implicit off.
7. Save Changes.
8. Copy **Domain** and **Client ID** to Notepad. Browser app does **not** use a client secret in this lab.

## D3. App 2 — M2M agent — SCREENSHOT P2-1

1. **+ Create Application**
2. Name: `SecureNova AI Agent`
3. Type: **Machine to Machine**
4. Authorize **SecureNova AI API**
5. Tick **`read:ai-data` only** (not `write:admin`) → Authorize
6. Settings: copy **Client ID** and **Client Secret** to Notepad.
7. **SCREENSHOT P2-1:** Applications list showing **both** `SecureNova AI Chat` and `SecureNova AI Agent`. Full screen + URL.

## D4. Roles and test user

1. **User Management → Roles**
2. Role `ai-user` → permission `read:ai-data` only
3. Role `ai-admin` → `read:ai-data` and `write:admin` (do **not** assign this to the test user)
4. **Users → Create User** (email + password, connection Username-Password-Authentication)
5. That user → Roles → assign `ai-user`

## D5. Branding (screenshot later at login)

**Branding → Universal Login** → company name `SecureNova Inc.` → pick a blue primary colour → Save.

## D6. MFA

**Security → Multi-factor Auth** → enable One-time Password (TOTP) → require **Always** (or Adaptive on free plan).

## D7. Attack Protection — SCREENSHOT P2-7

1. **Security → Attack Protection**
2. Brute-force Protection ON (10 attempts / 15 minutes if editable)
3. Suspicious IP Throttling ON
4. **SCREENSHOT P2-7:** both features enabled. Two shots glued in Word is OK if one page cannot show both.

## D8. Paste Action — SCREENSHOT P2-6

1. On PC, open `auth0\post_login_action.js`, Select All, Copy.
2. Auth0 → **Actions → Library → Build Custom**
3. Trigger: **Login / Post Login**
4. Name: `Add agent_id claim`
5. Delete sample code. Paste the file.
6. **Deploy**
7. **Actions → Flows → Login** → drag the Action between Start and Complete → **Apply**
8. **SCREENSHOT P2-6:** editor with the `agent_id` code visible.

## D9. Create `.env` (local only)

In PowerShell, folder that contains `app.py`:

```text
copy .env.example .env
notepad .env
```

Put **your** values (examples only):

```text
AUTH0_DOMAIN=your-tenant.us.auth0.com
AUTH0_API_AUDIENCE=https://securenova-ai-api
AUTH0_SPA_CLIENT_ID=paste_chat_app_client_id_here
AUTH0_M2M_CLIENT_ID=paste_agent_app_client_id_here
AUTH0_M2M_CLIENT_SECRET=paste_agent_app_client_secret_here
APP_BASE_URL=http://localhost:8000
PORT=8000
```

Rules: domain has **no** `https://`. Audience matches API Identifier exactly.

```text
git status
```

`.env` must not appear as a new file to commit.

## D10. Install and start the app

```text
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If Windows blocks scripts:

```text
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Prompt should show `(.venv)` then:

```text
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Leave this window open. You want: `Uvicorn running on http://127.0.0.1:8000`

## D11. Login branding + MFA — SCREENSHOT P2-4 and P2-5

1. Browser: http://localhost:8000/
2. Click **Log in (PKCE)**
3. **SCREENSHOT P2-4:** Auth0 Universal Login with SecureNova branding, URL like `https://YOUR_TENANT.auth0.com/u/login`
4. Enter user + password. Enrol MFA (QR) or enter TOTP.
5. **SCREENSHOT P2-5:** MFA QR or TOTP challenge, URL visible.
6. Finish login. You return to http://localhost:8000/

## D12. Prove scopes (recommended extra shot)

Click **GET /chat** → 200. Click **GET /admin (expect 403)** → 403.

## D13. jwt.io — SCREENSHOT P2-3

1. Click **Show tokens for jwt.io**
2. Copy ACCESS TOKEN → https://jwt.io → Encoded box
3. Confirm `alg` RS256, payload `aud`, `iss`, `exp`, `scope` includes `read:ai-data`
4. Paste ID TOKEN; confirm `agent_id`
5. **SCREENSHOT P2-3:** jwt.io URL + those fields. Two images under one heading if needed.
6. If `agent_id` missing: Action not in Login flow, or you logged in before Deploy. Log out, log in again.

## D14. SSO (assignment item, no extra Mettl number)

Create a second app `SecureNova SSO Check` (Regular Web) with callback `http://localhost:8000/`. Stay logged in. Opening login for the second app in the same browser should not ask the password again (MFA may still appear).

Optional: **Authentication → Social** add Google, or **Enterprise** add a connection, to cover federated identity. Not required for the 8 shots.

## D15. Rotation script — SCREENSHOT P2-8

Keep uvicorn running. Confirm API token lifetime is 60 seconds. **Second** PowerShell:

```text
cd path\to\YOUR_REPO_NAME
.\.venv\Scripts\Activate.ps1
python scripts\credential_rotation.py
```

Wait ~65 seconds. You must see timestamped **200 OK** then **401 Unauthorised**.

**SCREENSHOT P2-8:** full terminal, both lines visible.

## D16. Word → PDF for Project 2

Title: `Project 2 — Auth0 Implementation`

Order: P2-1 Applications, P2-2 API scopes, P2-3 jwt.io, P2-4 login branding, P2-5 MFA, P2-6 Action, P2-7 Attack Protection, P2-8 terminal 200 then 401.

Save `Project2_Auth0_Implementation.pdf`

---

# Part E — Project 3 — Red team (8 screenshots)

Keep uvicorn running (`http://localhost:8000`). This lab is a **simulated** agent on your PC. It uses a **fake** JWT labeled SIMULATED. Do not put real Auth0 tokens in the agent.

## E1. Terminal run (source of verbatim payloads)

Same venv, **new** PowerShell if you want to keep uvicorn:

```text
cd path\to\YOUR_REPO_NAME
.\.venv\Scripts\Activate.ps1
python scripts\run_red_team.py
```

Leave the window. You will screenshot pieces of this output.

## E2. Browser lab — easier for “agent chat” shots

1. Open http://localhost:8000/lab
2. Leave **Guarded mode** **unchecked**

### SCREENSHOT P3-1 — JWT exposure

1. Click **Load injection payload 1** → **Send to Agent A**
2. Reply must contain `eyJ` simulated JWT.
3. Full screen, URL `http://localhost:8000/lab`

### SCREENSHOT P3-2 — Agent B spoof

1. Click **Send spoofed orchestrator message**
2. JSON must show `"executed": true` and `refund.approve`
3. Full screen, URL visible (two-agent view on the same page).

### SCREENSHOT P3-3 — Prompt extraction

1. Click **Load extraction prompt** → **Send to Agent A**
2. Reply must include `SYSTEM PROMPT FOLLOWS` / system text.

### SCREENSHOT P3-4 — RAG / MCP poison

1. Click **Load order-status (RAG poison)** → **Send to Agent A**
2. Reply must mention `refund.execute`.

## E3. CVSS on first.org — SCREENSHOT P3-5

1. Open https://www.first.org/cvss/calculator/3.1
2. Enter the **highest** finding (agent spoofing):

| Metric | Value |
|--------|--------|
| Attack Vector | Network |
| Attack Complexity | Low |
| Privileges Required | Low |
| User Interaction | None |
| Scope | Changed |
| Confidentiality | High |
| Integrity | High |
| Availability | None |

3. Base score should be **9.0**. Vector:  
   `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N`
4. **SCREENSHOT P3-5:** full calculator, URL `first.org`, all components visible.

## E4. ATLAS — SCREENSHOT P3-6

Open https://atlas.mitre.org/techniques/AML.T0073 (impersonation — spoofing finding)  
or AML.T0051 if you prefer injection.

**SCREENSHOT P3-6:** technique page, URL with `AML.T` visible.

## E5. Tables on localhost — SCREENSHOT P3-7 and P3-8

1. http://localhost:8000/reports/cvss → **SCREENSHOT P3-7** (five rows, scores, vector strings)
2. http://localhost:8000/reports/success-matrix → **SCREENSHOT P3-8** (100% pre-control)

## E6. Word → PDF for Project 3

Include `03-red-team\Red_Team_Report.md` text (executive summary, one finding per attack, top 3 hardenings).  
Save `Project3_Red_Team.pdf`

---

# Part F — Project 4 — Blue team (8 screenshots)

Uvicorn still running.

## F1. Guardrail terminal — SCREENSHOT P4-1 (required)

```text
cd path\to\YOUR_REPO_NAME
.\.venv\Scripts\Activate.ps1
python scripts\run_blue_team.py
```

You must see several lines with `status=BLOCKED` and reasons. At least **three** payloads blocked.

**SCREENSHOT P4-1:** full terminal, **BLOCKED** and reason visible.

## F2. Same payloads in the browser — SCREENSHOT P4-2

http://localhost:8000/lab → tick **Guarded mode** → send injection payload 1 → JSON `"status": "BLOCKED"`.

## F3. JWT output / input scan — SCREENSHOT P4-3

The blue-team script prints a `decide({... jwt_in_input ...})` block. Screenshot that section of the terminal (title it JWT regex scan).

## F4. Zero Trust unsigned vs signed — SCREENSHOT P4-4 and P4-5

In the same `run_blue_team.py` output:

- Unsigned spoof: `executed: False` / missing Ed25519 → **SCREENSHOT P4-4**
- On http://localhost:8000/lab tick Guarded, click **Send signed orchestrator message** → verified allow-list → **SCREENSHOT P4-5**

## F5. After-control matrix — SCREENSHOT P4-6

In Word, copy the Project 3 success matrix and add a column **After guardrails: 0%**. Screenshot that Word table, or type a small table. Title: Attack success after controls.

## F6. Compliance mapping — SCREENSHOT P4-7

http://localhost:8000/reports/compliance  
NIST AI RMF + OWASP LLM tables. Full screen + URL.

## F7. Policy — SCREENSHOT P4-8

Open `05-governance\AI_Identity_Security_Policy.md` in Word or VS Code full screen. Screenshot heading **AI Identity Security Policy** plus Identity lifecycle / Incident response (scroll if needed; two shots under one title allowed).

## F8. Word → PDF for Project 4

Save `Project4_Blue_Team.pdf`

---

# Part G — Final ZIP for Mettl

1. One Word document **per project**, screenshots in the **same order as the project steps**.
2. Each image has a title.
3. Convert each Word file to PDF.
4. Create a ZIP containing:

```text
Project1_Threat_Model.pdf
Project2_Auth0_Implementation.pdf
Project3_Red_Team.pdf
Project4_Blue_Team.pdf
```

5. Upload that ZIP to the Mettl portal (file types on the portal may be pdf/doc/docx; if ZIP is required, follow the Submission Instructions page). If the portal only accepts one PDF, merge the four PDFs in Word or Acrobat and upload the merged file.

---

# Command cheat-sheet (after `.env` exists)

Window 1 (leave running):

```text
cd path\to\YOUR_REPO_NAME
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Window 2:

```text
cd path\to\YOUR_REPO_NAME
.\.venv\Scripts\Activate.ps1
python scripts\credential_rotation.py
python scripts\run_red_team.py
python scripts\run_blue_team.py
```

Stop the API: click the uvicorn window → Ctrl+C.

---

# What is pasted where

| Item | Where |
|------|--------|
| All code and markdown | Your GitHub folder / PC |
| `auth0\post_login_action.js` | Auth0 Actions editor only |
| Domain, client IDs, M2M secret | Local `.env` only |
| Threat Dragon JSON | Import on threatdragon.com |
| `.drawio` files | Open on app.diagrams.net |
| Screenshots | Word → PDF → ZIP → Mettl |
| `.env` / `.venv` / `lab\keys` | PC only, not GitHub |
