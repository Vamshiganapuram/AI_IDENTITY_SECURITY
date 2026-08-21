# Project 2 — Complete start-to-finish (do this in order)

Nothing is assumed done except: you created a **GitHub repository** and this project folder is in it.

You do **not** import this GitHub repo into Auth0.  
Auth0 is a website you configure by clicking.  
This GitHub repo is the **local AI chat app** you run on your PC.

**The only file you copy into Auth0** is `auth0/post_login_action.js` (Step 12).  
**Never put `.env` or client secrets on GitHub.**

Mettl screenshots: **full screen**, **address bar visible**, take them at the steps marked **SCREENSHOT**.

---

## Step 0 — Install Python on Windows

1. Open https://www.python.org/downloads/
2. Download Python 3.12 or 3.13.
3. Run the installer.
4. Tick **Add python.exe to PATH**.
5. Click Install Now. Finish.

Open **PowerShell** (Windows key, type `PowerShell`, Enter) and run:

```text
python --version
pip --version
```

You must see version numbers. If `python` is not found, close PowerShell, open a **new** PowerShell window, try again. If it still fails, reinstall Python and tick **Add to PATH**.

---

## Step 1 — Open the GitHub project on your PC

In PowerShell:

```text
cd path\to\your\cloned\repo
```

Example if the folder is on the Desktop:

```text
cd $HOME\Desktop\project2-auth0-ai-app
```

List files (confirm they exist):

```text
dir
```

You should see:

| Already in GitHub (do not recreate) | What it is |
|-------------------------------------|------------|
| `app.py` | Chat API on your PC |
| `requirements.txt` | Python libraries to install |
| `.env.example` | Template for secrets (safe to keep on GitHub) |
| `.gitignore` | Stops `.env` being uploaded |
| `static\index.html` | Login page in the browser |
| `static\app.js` | PKCE login code |
| `static\styles.css` | Page styling |
| `scripts\credential_rotation.py` | 200 then 401 evidence script |
| `auth0\post_login_action.js` | **Paste this into Auth0 later** |
| `START_HERE.md` | This guide |

If a file is missing, copy it from `C:\Users\asus\Documents\project2-auth0-ai-app` into the GitHub folder.

You will **create locally** (not on GitHub):

| You create | When |
|------------|------|
| `.env` | Step 13 |
| `.venv\` folder | Step 14 (Python makes this) |

---

## Step 2 — Create a free Auth0 account and tenant

1. Open https://auth0.com in Chrome or Edge.
2. Click **Sign up** (or **Login** if you already have an account).
3. Use email + password or GitHub/Google.
4. If asked to create a **tenant**:
   - Tenant Domain: `securenova-ai` (any unique name is fine)
   - Region: pick the closest (US / Europe / Australia)
   - Environment: **Development**
5. Finish until you see the Auth0 **Dashboard** (left sidebar: Getting Started, Applications, Branding, Security, …).

Your domain looks like: `securenova-ai.us.auth0.com`  
Write that domain in Notepad. You need it in `.env`.

---

## Step 3 — Create the API and two scopes

This is the “AI chat API” that tokens are issued for.

1. Left sidebar: **Applications** → **APIs**.
2. Click **+ Create API**.
3. Fill in:
   - **Name:** `SecureNova AI API`
   - **Identifier:** `https://securenova-ai-api`  
     Copy this **exactly**. It becomes `AUTH0_API_AUDIENCE`.
   - **JSON Web Token (JWT) Profile:** leave default.
   - **Signing Algorithm:** `RS256`
4. Click **Create**.

### Add scopes (Auth0 calls them Permissions)

1. Open **SecureNova AI API**.
2. Tab **Permissions**.
3. Add permission:
   - Permission: `read:ai-data`
   - Description: `User-level AI chat data`
   - Click **Add**.
4. Add permission:
   - Permission: `write:admin`
   - Description: `Admin-level operations`
   - Click **Add**.

### API settings required for this project

1. Same API → tab **Settings**.
2. **Token Expiration (Seconds):** type `60` (needed for the 401 replay).
3. Scroll to **RBAC Settings**:
   - Turn **Enable RBAC** ON.
   - Turn **Add Permissions in the Access Token** ON.
4. Click **Save**.

**SCREENSHOT 2 (now)**  
Full screen. URL bar showing Auth0. API **Permissions** tab with **both** `read:ai-data` and `write:admin` visible.

---

## Step 4 — Create application 1: Regular Web App (AI chat)

Assignment wording: Regular Web Application.  
This project’s browser login uses **PKCE**, which Auth0 implements as a **Single Page Application**. You create the web app, then set the type so login works.

1. Left sidebar: **Applications** → **Applications**.
2. Click **+ Create Application**.
3. **Name:** `SecureNova AI Chat`
4. Choose **Regular Web Applications**.
5. Click **Create**.
6. Open the app → tab **Settings**.
7. Find **Application Type**. Change it to **Single Page Application**.  
   If the dashboard will not change type, click **Create Application** again, name it `SecureNova AI Chat`, choose **Single Page Application**, and use that one as the chat app. Keep any extra unused app or delete it so the Applications list stays clear.
8. Scroll to **Application URIs**. Paste these **exactly** (include the trailing slash on callback):

| Field | Value |
|--------|--------|
| Allowed Callback URLs | `http://localhost:8000/` |
| Allowed Logout URLs | `http://localhost:8000/` |
| Allowed Web Origins | `http://localhost:8000` |
| Allowed Origins (CORS) | `http://localhost:8000` |

9. Scroll to **Advanced Settings** → **Grant Types**. Tick:
   - Authorization Code
   - Refresh Token
   - Untick Implicit if it is ticked.
10. Click **Save Changes**.
11. At the top of Settings, copy **Domain** and **Client ID** into Notepad.  
    There is **no Client Secret** used by the browser app.

---

## Step 5 — Create application 2: Machine-to-Machine (AI agent)

1. **Applications** → **Applications** → **+ Create Application**.
2. **Name:** `SecureNova AI Agent`
3. Choose **Machine to Machine Applications**.
4. Click **Create**.
5. Auth0 asks which API to authorize. Select **SecureNova AI API**.
6. Tick permission **`read:ai-data` only**. Do **not** tick `write:admin`.
7. Click **Authorize**.
8. Open **SecureNova AI Agent** → **Settings**.
9. Copy **Client ID** and **Client Secret** into Notepad (secret is shown once / behind a reveal).

If authorize was skipped: open the M2M app → tab **APIs** → authorize **SecureNova AI API** with `read:ai-data`.

**SCREENSHOT 1 (now)**  
**Applications** → **Applications** list. Both **SecureNova AI Chat** and **SecureNova AI Agent** visible. Full screen + URL.

---

## Step 6 — Allow the chat app to request the API

1. Open **SecureNova AI Chat** (the SPA / web app).
2. Tab **APIs** (or **Machine to Machine Applications** is the wrong tab — stay on the chat app).
3. Find **SecureNova AI API** and set it **Authorized**.
4. If you can pick permissions for the user app, allow **`read:ai-data` only**.

If there is no APIs tab on the SPA: it is enough that the API identifier is requested as `audience` from the app (already in our code) and RBAC is on.

---

## Step 7 — Create roles so a normal user cannot call admin

1. Left sidebar: **User Management** → **Roles**.
2. **+ Create Role**
   - Name: `ai-user`
   - Description: `Customer chat user`
   - Create.
3. Open `ai-user` → tab **Permissions** → **Add Permissions**.
4. Select API **SecureNova AI API**.
5. Tick **`read:ai-data` only** → Add.
6. **+ Create Role** again:
   - Name: `ai-admin`
   - Add permissions `read:ai-data` **and** `write:admin`.
7. Do **not** assign `ai-admin` to your test user.

---

## Step 8 — Create a test user and assign `ai-user`

1. **User Management** → **Users** → **+ Create User**.
2. Email: a real email you can use (or `demo@example.com` if Auth0 allows it).
3. Password: something you will remember (meets Auth0 rules).
4. Connection: **Username-Password-Authentication**.
5. Create.
6. Open that user → tab **Roles** → **Assign Roles** → `ai-user` → Assign.

---

## Step 9 — Universal Login branding

1. Left sidebar: **Branding** → **Universal Login**.
2. Click **Customize** / **Advanced Options** / **Settings** (wording varies).
3. Set:
   - **Primary color** (any SecureNova-looking blue).
   - **Page background**.
   - **Company Name:** `SecureNova Inc.`
4. Save.

You take the branding **screenshot later at login** (Step 16), not on this settings page, because Mettl wants the **login page in the browser**.

---

## Step 10 — Turn on TOTP MFA

1. **Security** → **Multi-factor Auth**.
2. Enable **One-time Password** (authenticator app / TOTP).
3. Policy: **Always** require MFA.  
   If **Always** is locked on the free plan, use **Adaptive** and still enrol MFA for your user (Step 16).
4. Save.

Install **Google Authenticator** or **Microsoft Authenticator** on your phone before you log in.

---

## Step 11 — Attack Protection

1. **Security** → **Attack Protection**.
2. Open **Brute-force Protection**:
   - Toggle **ON**.
   - If you can edit numbers: max **10** attempts, lockout **15 minutes**.
   - Save.
3. Open **Suspicious IP Throttling**:
   - Toggle **ON**.
   - Save.

**SCREENSHOT 7 (now)**  
Attack Protection so **both** Brute-Force Protection and Suspicious IP Throttling show as enabled. If one page cannot show both, take two shots and put them together in Word with the same title. Prefer one overview if both are visible.

---

## Step 12 — Auth0 Action: paste `agent_id` (only file you paste)

1. On your PC, open this file in Notepad or VS Code:

`auth0\post_login_action.js`

2. Select all and copy.

3. In Auth0: **Actions** → **Library** (or **Actions** → **Custom**).
4. **Build Custom** / **Create Action**.
5. Choose trigger **Login / Post Login**.
6. Name: `Add agent_id claim`
7. Trigger: **Login / Post Login**.
8. Create.
9. Delete any sample code in the editor.
10. Paste the file contents. It must look like:

```javascript
exports.onExecutePostLogin = async (event, api) => {
  const namespace = "";
  const agentId = `sn-agent-${event.user.user_id}`;

  api.idToken.setCustomClaim(`${namespace}agent_id`, agentId);
  api.accessToken.setCustomClaim(`${namespace}agent_id`, agentId);
};
```

11. Click **Deploy**.
12. **Actions** → **Flows** → **Login**.
13. Drag **Add agent_id claim** from the right into the flow **between Start and Complete**.
14. Click **Apply**.

**SCREENSHOT 6 (now)**  
Actions editor with that code visible. Full screen + URL.

---

## Step 13 — Create `.env` on your PC (never commit this)

In PowerShell, from the **repo root** (the folder that contains `app.py`):

```text
copy .env.example .env
notepad .env
```

Replace every `replace_with_...` value. Finished file looks like this (use **your** values):

```text
AUTH0_DOMAIN=securenova-ai.us.auth0.com
AUTH0_API_AUDIENCE=https://securenova-ai-api
AUTH0_SPA_CLIENT_ID=paste_chat_app_client_id_here
AUTH0_M2M_CLIENT_ID=paste_agent_app_client_id_here
AUTH0_M2M_CLIENT_SECRET=paste_agent_app_client_secret_here
APP_BASE_URL=http://localhost:8000
PORT=8000
```

Rules:

- `AUTH0_DOMAIN` has **no** `https://`.
- `AUTH0_API_AUDIENCE` is **exactly** the API Identifier from Step 3.
- `AUTH0_SPA_CLIENT_ID` is from **SecureNova AI Chat**.
- M2M id + secret are from **SecureNova AI Agent**.
- Save and close Notepad.

Confirm `.env` will not go to GitHub:

```text
git status
```

`.env` must **not** appear as a new file to commit. If it does, `.gitignore` is missing the line `.env` — add it, then `git status` again.

---

## Step 14 — Install libraries and start the chat API

Same PowerShell, repo root:

```text
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If Windows blocks the script:

```text
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Your prompt should start with `(.venv)`. Then:

```text
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Leave this window **open**. You should see something like `Uvicorn running on http://127.0.0.1:8000`.

If port 8000 is busy, close the other program or tell me the error text.

---

## Step 15 — Open the app

1. Open a **new** browser window (Chrome/Edge).
2. Go to **exactly:** http://localhost:8000/
3. You should see **SecureNova Inc. / AI Chat Service**.
4. Click **Log in (PKCE)**.

If the page is blank or Auth0 errors:

- Wrong Client ID or Domain in `.env` (restart uvicorn after saving `.env`).
- Callback URL mismatch (must be `http://localhost:8000/` with slash).
- API Identifier mismatch.

---

## Step 16 — Login page branding + MFA (two screenshots)

After clicking Log in you land on Auth0 (URL like `https://YOUR_TENANT.auth0.com/u/login`).

**SCREENSHOT 4 (now)**  
Full screen. Auth0 Universal Login with **SecureNova** branding. Address bar visible.

Then:

1. Enter the test user email and password.
2. Auth0 will ask to **enrol MFA** (QR code) or enter a **TOTP code**.

**SCREENSHOT 5 (now)**  
Full screen. MFA enrolment QR **or** TOTP challenge. Address bar visible.

3. Scan the QR with the authenticator app, enter the 6-digit code, continue.
4. You return to http://localhost:8000/ signed in.

---

## Step 17 — Prove PKCE scopes (403 on admin)

On http://localhost:8000/ :

1. Click **GET /chat** — status **200**.
2. Click **GET /admin (expect 403)** — status **403**.

Optional extra screenshot for Word: this 403 page/output (brief asked for 9 shots but listed 8).

---

## Step 18 — jwt.io (screenshot 3)

1. Still on http://localhost:8000/ click **Show tokens for jwt.io**.
2. Copy the **ACCESS TOKEN** (long string after `===== ACCESS TOKEN =====`).
3. Open https://jwt.io in another tab.
4. Paste into the left **Encoded** box.
5. Confirm **header** `alg` is `RS256`.
6. Confirm **payload** has `aud`, `iss`, `exp`, `scope` (`read:ai-data`).
7. If `agent_id` is missing on the access token, paste the **ID TOKEN** instead. The ID token must show `agent_id`.

**SCREENSHOT 3 (now)**  
jwt.io full screen. URL `https://jwt.io`. Payload showing `aud`, `iss`, `exp`, `scope`, and `agent_id`. If one token cannot show all fields, put access-token decode and ID-token decode as two images under one title.

If `agent_id` is missing: the Login Action is not in the Login **flow**, or you logged in **before** deploying it. Log out, log in again.

---

## Step 19 — SSO (assignment item 5, no extra Mettl number)

1. Auth0 → **Applications** → **Create Application**.
2. Name: `SecureNova SSO Check`.
3. Type: **Regular Web Applications** (leave this one as Regular Web).
4. Same callback URLs as the chat app: `http://localhost:8000/`.
5. Save.
6. **Authentication** → **Settings** (or tenant **Settings**): SSO is on by default for one tenant.
7. Stay logged into the chat app. Opening login for the second app in the same browser should **not** ask for password again (it may still ask MFA depending on settings).

You do not need a screenshot unless your instructor asked for SSO evidence beyond the listed 8.

---

## Step 20 — Credential rotation script (screenshot 8)

1. Confirm **SecureNova AI API** token expiration is still **60** seconds (Step 3).
2. Confirm **uvicorn is still running** in the first PowerShell.
3. Open a **second** PowerShell:

```text
cd path\to\your\cloned\repo
.\.venv\Scripts\Activate.ps1
python scripts\credential_rotation.py
```

Wait about **65 seconds**. Do not close the window.

You must see timestamped lines:

- First `/chat` → **HTTP 200 OK**
- After the wait, replay → **HTTP 401** and text **Unauthorised**

**SCREENSHOT 8 (now)**  
Full **terminal** window. Timestamps visible. Both 200 and 401 in the same shot if possible. If the window scrolled, make the window taller or take two shots titled as one step.

If the second call is still 200: token lifetime is longer than 60s — set API expiration to 60, wait a minute, run the script again.

If the first call is 401/403: M2M app is not authorized for `read:ai-data`, or `.env` M2M values are wrong.

---

## Step 21 — Word document → PDF → ZIP (submission)

1. Open Microsoft Word. New blank document. Title: `Project 2 — Auth0 Implementation`.
2. Paste screenshots **in this order**, each with a heading:

| Order in Word | Heading to type under the image |
|---------------|----------------------------------|
| 1 | Auth0 Applications page — Regular Web App and M2M app |
| 2 | Auth0 APIs page — scopes read:ai-data and write:admin |
| 3 | jwt.io — RS256, aud, iss, exp, scope, agent_id |
| 4 | Auth0 Universal Login — SecureNova branding |
| 5 | Auth0 MFA enrolment or TOTP challenge |
| 6 | Auth0 Actions editor — agent_id post-login Action |
| 7 | Auth0 Attack Protection — brute-force and suspicious IP throttling |
| 8 | Terminal — credential rotation 200 OK then 401 Unauthorised |

3. File → Save As → PDF: `Project2_Auth0_Implementation.pdf`.
4. Put that PDF (and Project 1 PDF if required) in a ZIP.
5. Upload the ZIP to Mettl.

---

## Command cheat-sheet (after Step 13)

```text
cd path\to\your\cloned\repo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Second window:

```text
cd path\to\your\cloned\repo
.\.venv\Scripts\Activate.ps1
python scripts\credential_rotation.py
```

Stop the API: click the uvicorn window and press `Ctrl+C`.

---

## What goes where (summary)

| Thing | Where it goes |
|--------|----------------|
| All project `.py`, `.html`, `.js`, `.md` | Already in GitHub. Do not paste them into Auth0. |
| `auth0\post_login_action.js` | Copy-paste into Auth0 **Actions** editor only. |
| Domain, Client IDs, M2M secret | Your local `.env` only. |
| Screenshots | Word → PDF → ZIP → Mettl. Not required on GitHub. |
| `.venv` and `.env` | Local PC only. Not GitHub. |
