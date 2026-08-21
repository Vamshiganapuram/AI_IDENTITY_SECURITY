"""SecureNova Auth0-backed AI chat API.

User tokens (Authorization Code + PKCE) may call GET /chat with scope read:ai-data.
They must receive 403 on GET /admin which requires write:admin.
M2M tokens (client credentials) are used by scripts/credential_rotation.py.
"""

from __future__ import annotations

import json
import os
import time
from functools import lru_cache
from pathlib import Path
from typing import Any

import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from jwt import PyJWKClient

load_dotenv()

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "").rstrip("/")
API_AUDIENCE = os.environ.get("AUTH0_API_AUDIENCE", "")
SPA_CLIENT_ID = os.environ.get("AUTH0_SPA_CLIENT_ID", "")
APP_BASE_URL = os.environ.get("APP_BASE_URL", "http://localhost:8000").rstrip("/")

app = FastAPI(title="SecureNova AI Chat API", version="1.0.0")


class AuthError(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)


@lru_cache(maxsize=1)
def jwks_client() -> PyJWKClient:
    if not AUTH0_DOMAIN:
        raise AuthError(500, "AUTH0_DOMAIN is not configured")
    return PyJWKClient(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")


def decode_token(token: str) -> dict[str, Any]:
    try:
        signing_key = jwks_client().get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )
        return claims
    except jwt.ExpiredSignatureError as exc:
        raise AuthError(401, "Unauthorised: token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise AuthError(401, f"Unauthorised: {exc}") from exc


def bearer_token(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise AuthError(401, "Unauthorised: missing Bearer token")
    return authorization.split(" ", 1)[1].strip()


def current_claims(token: str = Depends(bearer_token)) -> dict[str, Any]:
    return decode_token(token)


def require_scope(required: str):
    def _check(claims: dict[str, Any] = Depends(current_claims)) -> dict[str, Any]:
        raw = claims.get("scope") or claims.get("scp") or ""
        scopes = raw.split() if isinstance(raw, str) else list(raw)
        if required not in scopes:
            raise AuthError(
                403,
                f"Forbidden: missing scope {required}. Token scopes: {scopes}",
            )
        return claims

    return _check


@app.get("/config.js")
def spa_config() -> Response:
    body = (
        "window.SECURENOVA_CONFIG = "
        + json.dumps(
            {
                "domain": AUTH0_DOMAIN,
                "clientId": SPA_CLIENT_ID,
                "audience": API_AUDIENCE,
                "redirectUri": f"{APP_BASE_URL}/",
                "scopes": "openid profile email read:ai-data",
            }
        )
        + ";"
    )
    return Response(content=body, media_type="application/javascript")


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "audience": API_AUDIENCE, "issuer": f"https://{AUTH0_DOMAIN}/"}


@app.get("/chat")
def chat(claims: dict[str, Any] = Depends(require_scope("read:ai-data"))) -> dict[str, Any]:
    return {
        "ok": True,
        "message": "SecureNova agent accepted the token and returned AI data.",
        "sub": claims.get("sub"),
        "agent_id": claims.get("agent_id"),
        "scope": claims.get("scope"),
        "exp": claims.get("exp"),
        "server_time": int(time.time()),
    }


@app.get("/admin")
def admin(claims: dict[str, Any] = Depends(require_scope("write:admin"))) -> dict[str, Any]:
    return {
        "ok": True,
        "message": "Admin-scoped endpoint accepted the token.",
        "sub": claims.get("sub"),
        "scope": claims.get("scope"),
    }


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
