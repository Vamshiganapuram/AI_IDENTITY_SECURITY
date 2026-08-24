"""Obtain a short-lived M2M token, call /chat (200), wait, replay (401).

Set the Auth0 API Access Token Expiration to 60 seconds before running this
script so the replay after ~65 seconds is expired.

Evidence for Mettl: keep the terminal full-screen with timestamps visible.
"""

from __future__ import annotations

import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"].rstrip("/")
AUDIENCE = os.environ["AUTH0_API_AUDIENCE"]
CLIENT_ID = os.environ["AUTH0_M2M_CLIENT_ID"]
CLIENT_SECRET = os.environ["AUTH0_M2M_CLIENT_SECRET"]
API_BASE = os.environ.get("APP_BASE_URL", "http://localhost:8000").rstrip("/")


def ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def log(msg: str) -> None:
    print(f"[{ts()}] {msg}", flush=True)


def get_m2m_token() -> str:
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": AUDIENCE,
    }
    log(f"Requesting M2M token from {url} (TTL should be 60 seconds in Auth0)")
    resp = httpx.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    log(
        f"Token issued: token_type={data.get('token_type')} "
        f"expires_in={data.get('expires_in')}s"
    )
    return data["access_token"]


def call_chat(token: str) -> httpx.Response:
    return httpx.get(
        f"{API_BASE}/chat",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )


def main() -> int:
    log("SecureNova credential rotation evidence script starting")
    token = get_m2m_token()

    first = call_chat(token)
    log(f"First /chat call → HTTP {first.status_code} {first.reason_phrase}")
    log(f"Body: {first.text[:400]}")
    if first.status_code != 200:
        log("Expected 200 OK on the first call. Check M2M grants include read:ai-data.")
        return 1

    wait_s = 65
    log(f"Waiting {wait_s} seconds for the short-lived token to expire...")
    time.sleep(wait_s)

    second = call_chat(token)
    log(f"Replay /chat with expired token → HTTP {second.status_code} {second.reason_phrase}")
    log(f"Body: {second.text[:400]}")
    if second.status_code != 401:
        log("Expected 401 Unauthorised on replay. Confirm API token lifetime is 60s.")
        return 1

    log("Rotation evidence complete: 200 OK then 401 Unauthorised.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
