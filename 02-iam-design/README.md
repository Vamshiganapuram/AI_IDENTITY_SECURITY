# SecureNova Inc. — AI Identity Security capstone

**Start here:** open `COMPLETE_WALKTHROUGH.md` and follow Parts A–G in order.

This repository is the whole lab (threat model, Auth0-backed chat, red/blue agent simulator, governance).

- Do **not** import this GitHub repo into Auth0.
- The only Auth0 paste is `auth0/post_login_action.js`.
- Never commit `.env`.

After Auth0 values are in `.env`:

```text
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Then open http://localhost:8000/ (Project 2 login) and http://localhost:8000/lab (Projects 3–4).
