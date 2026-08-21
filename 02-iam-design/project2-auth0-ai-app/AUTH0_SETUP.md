# Project 2 — Auth0 dashboard setup

Do these steps in a **free Auth0** tenant. Keep the **full browser window** (URL bar) visible for screenshots.

## 1. Create the tenant

1. Sign up at https://auth0.com (Developer / free).
2. Tenant name example: `securenova-ai-identity`.
3. Region: closest to you (US / EU / AU). Domain will look like `securenova-ai-identity.us.auth0.com`.

## 2. Register applications (screenshot 1)

**Applications → Applications → Create Application**

| App | Type | Used for |
|-----|------|----------|
| SecureNova AI Chat | **Single Page Application** | User login, Authorization Code + PKCE |
| SecureNova AI Agent | **Machine to Machine** | Short-lived agent token |

If the brief says “Regular Web Application”, you may create that type instead of SPA. For this lab the SPA type is the correct match for PKCE in the browser. If you must use Regular Web App, still enable PKCE and use the same callback URLs.

For **SecureNova AI Chat**:

- Allowed Callback URLs: `http://localhost:8000/`
- Allowed Logout URLs: `http://localhost:8000/`
- Allowed Web Origins: `http://localhost:8000`
- Allowed Origins (CORS): `http://localhost:8000`

Grant types: Authorization Code, Refresh Token, (implicit off).

For **SecureNova AI Agent** (M2M):

- Authorize it against the API in the next section.
- Grant type: Client Credentials.

Copy Client ID (SPA) and Client ID + Secret (M2M) into `.env`.

Optional third app for SSO evidence: another SPA with the same callbacks. After login to the chat app, open the second app — Auth0 should not prompt for password again (SSO).

## 3. Register the API and custom scopes (screenshot 2)

**Applications → APIs → Create API**

- Name: `SecureNova AI API`
- Identifier (Audience): `https://securenova-ai-api`  (must match `.env` `AUTH0_API_AUDIENCE`)
- Signing Algorithm: **RS256**

**Permissions** tab — add:

| Permission | Description |
|------------|-------------|
| `read:ai-data` | User-level AI chat data |
| `write:admin` | Admin-level operations |

**Settings** for the API:

- Token Expiration (Seconds): **60** for the rotation demo (you can raise it after the screenshot).
- Allow Skipping User Consent: on for the SPA (localhost).
- Enable RBAC: on.
- Add Permissions in the Access Token: **on**.

Authorize the M2M app on this API and grant **`read:ai-data`** (not `write:admin`).

For the SPA, under **APIs** (or Application → APIs) allow `read:ai-data` only. Do **not** grant `write:admin` to the user login so `/admin` returns 403.

## 4. Roles (so users never get write:admin)

**User Management → Roles**

- Role `ai-user` → permission `read:ai-data`
- Role `ai-admin` → `read:ai-data` and `write:admin` (do not assign this to your demo user)

Assign `ai-user` to your test user.

Enable **RBAC** on the API as above so scopes in the access token match the role.

## 5. Universal Login branding (screenshot 4)

**Branding → Universal Login**

- Customize the New Universal Login page.
- Company name: **SecureNova Inc.**
- Logo (optional) and primary colour.
- Save, then open the chat app login so the branded page is in the URL bar.

## 6. MFA (screenshot 5)

**Security → Multi-factor Auth**

- Factor: **One-time Password (TOTP)** — Authenticator app.
- Require MFA: **Always** (or Adaptive if Always is not on the free plan; then enrol MFA on the user).

Enrol a user with Google Authenticator / Microsoft Authenticator. Capture the enrolment QR **or** the TOTP challenge.

## 7. Attack Protection (screenshot 7)

**Security → Attack Protection**

- **Brute-force Protection**: On. Max **10** attempts, **15-minute** lockout (or closest settings on the free plan).
- **Suspicious IP Throttling**: On.

Screenshot the panel with both enabled.

## 8. Auth0 Action — `agent_id` (screenshot 6)

**Actions → Library → Build Custom → Login / Post Login**

Name: `Add agent_id claim`

Paste `auth0/post_login_action.js`.

**Actions → Flows → Login** — drop the Action into the flow, **Apply**.

Log in again, paste the **ID token** and **access token** into https://jwt.io (screenshot 3). Confirm:

- `alg` = **RS256**
- `aud` = `https://securenova-ai-api` (access token) or the SPA client ID (ID token)
- `iss` = `https://YOUR_TENANT/`
- `exp` present
- `scope` includes `read:ai-data` on the access token
- `agent_id` custom claim present

## 9. Fill `.env`

```text
copy .env.example .env
```

Then start the API and take the remaining screenshots from `SCREENSHOT_PLAYBOOK.md`.
