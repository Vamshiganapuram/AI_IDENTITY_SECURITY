# Project 2 — Build and Secure the Auth0-Backed AI Application

**Do the work in this order:** open `START_HERE.md` and follow Steps 0–21. That file assumes nothing except a GitHub clone of this folder.

SecureNova Inc. customer-service **AI chat** lab: Auth0 tenant, OAuth 2.0 **Authorization Code + PKCE**, custom scopes, MFA, attack protection, short-lived **M2M** tokens, and a post-login Action that adds `agent_id`.

Project 1 (threat model) stays in `Documents\project1-threat-model`. This folder is only Project 2.

## What you run locally

| Path | Purpose |
|------|---------|
| `app.py` | FastAPI: `GET /chat` (`read:ai-data`), `GET /admin` (`write:admin`) |
| `static/` | Browser PKCE login |
| `scripts/credential_rotation.py` | M2M token → 200 then expired replay → 401 |
| `auth0/post_login_action.js` | Paste into Auth0 Actions |
| `AUTH0_SETUP.md` | Dashboard clicks |
| `SCREENSHOT_PLAYBOOK.md` | Eight Mettl shots |

## Quick start

1. Complete `AUTH0_SETUP.md` and copy `.env.example` to `.env`.
2. Install and run:

```text
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

3. Open http://localhost:8000/ — **Log in (PKCE)** → **GET /chat** (200) → **GET /admin** (403).
4. Decode the access token at https://jwt.io.
5. Set API access-token lifetime to **60 seconds**, then:

```text
python scripts/credential_rotation.py
```

## Assignment coverage

1. **Tenant** — SPA (chat) + M2M (agent), callbacks, grants, CORS.
2. **PKCE** — Auth0 SPA SDK; user token rejected on admin with **403**.
3. **MFA + attack protection** — TOTP, brute-force (10 / 15 min), suspicious IP throttling.
4. **Credential rotation** — short-lived M2M, replay after 60s → **401 Unauthorised**.
5. **Actions** — `agent_id` on ID/access token; SSO via a second application in the same tenant.

Do not commit `.env` or client secrets.
