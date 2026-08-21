# Project 2 — Screenshot playbook (Mettl)

The brief lists **9 screenshots** and then **8 numbered items**. Capture the 8 listed shots in order, plus one extra (403 on `/admin`) if you want a ninth. Full screen. URL or terminal title visible. One Word document → PDF.

| # | Required shot | How |
|---|----------------|-----|
| 1 | Auth0 **Applications** page — Regular/SPA web app **and** M2M app both visible | Dashboard → Applications. Zoom so both names show. |
| 2 | Auth0 **APIs** page — scopes `read:ai-data` and `write:admin` | Open SecureNova AI API → Permissions. |
| 3 | **jwt.io** — `aud`, `iss`, `exp`, `scope`, `agent_id`, alg RS256 | After login, **Show access token** (and also decode the ID token if `agent_id` is only on the ID token). URL `https://jwt.io`. |
| 4 | Universal Login **custom branding** | Click Log in on `http://localhost:8000/` so Auth0 hosted login shows SecureNova branding. |
| 5 | **MFA** enrolment or TOTP challenge | First login after MFA is required, or Security → MFA while a challenge is on screen. |
| 6 | **Actions** editor — post-login code adding `agent_id` | Open the Action; entire function visible. |
| 7 | **Attack Protection** — brute-force **and** suspicious IP throttling on | Security → Attack Protection; open both panels or overview showing both enabled. Max 10 attempts / 15-minute lockout visible if the UI shows it. |
| 8 | **Terminal** — rotation script: timestamped **200 OK** then **401 Unauthorised** | API running; Auth0 API token TTL = 60s; `python scripts/credential_rotation.py`. |

## Extra (recommended 9th)

Browser or terminal: user token calling `GET /admin` returning **403**.

## Word → PDF

1. Title each screenshot with the table text above.
2. Same order as the project steps.
3. Save as `Project2_Auth0_Implementation.pdf`.
4. ZIP with the other project PDFs for Mettl.
