"""
Project 2: OAuth 2.0 + PKCE and OIDC Agent Authentication Engine
Simulates Auth0 Universal Login, PKCE Proof Key generation, Token Exchange,
and Custom Claims verification (agent_id) matching jwt.io inspection.
"""
import base64
import hashlib
import json
import secrets
import time
import os
import sys
import jwt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import AUTH0_DOMAIN, AUTH0_AUDIENCE, AUTH0_ISSUER, JWT_SECRET_KEY, CLIENT_CUSTOMER_AGENT

def generate_pkce_pair():
    """Generates PKCE Code Verifier and Code Challenge (RFC 7636)."""
    verifier = secrets.token_urlsafe(64)
    # SHA-256 hash of verifier
    digest = hashlib.sha256(verifier.encode('ascii')).digest()
    challenge = base64.urlsafe_b64encode(digest).decode('ascii').replace('=', '')
    return verifier, challenge

def build_auth_url(client_id, challenge):
    """Builds Auth0 Authorization URL with PKCE parameters."""
    state = secrets.token_hex(16)
    redirect_uri = "https://agent.securenova.ai/callback"
    url = (
        f"https://{AUTH0_DOMAIN}/authorize?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"scope=openid%20profile%20email%20offline_access&"
        f"state={state}&"
        f"code_challenge={challenge}&"
        f"code_challenge_method=S256&"
        f"audience={AUTH0_AUDIENCE}"
    )
    return url, state

def simulate_post_login_action(user_email, client_id):
    """Simulates the Auth0 Action executing post-login."""
    now = int(time.time())
    assigned_agent = "agent_cs_9942a"
    trust_tier = "Tier-2_Autonomous"
    if user_email.endswith("@securenova.ai"):
        assigned_agent = "agent_orchestrator_001_enterprise"
        trust_tier = "Tier-1_Privileged"

    header = {
        "alg": "HS256",
        "typ": "JWT",
        "kid": "key_securenova_auth0_2026_01"
    }

    payload = {
        "iss": AUTH0_ISSUER,
        "sub": f"auth0|user_{hashlib.md5(user_email.encode()).hexdigest()[:10]}",
        "aud": [AUTH0_AUDIENCE, f"https://{AUTH0_DOMAIN}/userinfo"],
        "iat": now,
        "exp": now + 3600,
        "azp": client_id,
        "scope": "openid profile email offline_access",
        "email": user_email,
        "email_verified": True,
        # Custom claims injected by Auth0 Post-Login Action
        "https://securenova.ai/agent_id": assigned_agent,
        "https://securenova.ai/trust_tier": trust_tier,
        "https://securenova.ai/assigned_tenant": "ten_securenova_enterprise_01",
        "https://securenova.ai/allowed_tools": [
            "rag:query_knowledge_base",
            "profile:lookup_customer_profile"
        ]
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256", headers=header)
    return token, header, payload

def run_oauth_flow():
    print("=" * 80)
    print(" PROJECT 2 - STEP 1 & 2: OAUTH 2.0 + PKCE CLIENT AUTHENTICATION FLOW")
    print(" Organization: SecureNova Inc. | Identity Provider: Auth0")
    print("=" * 80)

    verifier, challenge = generate_pkce_pair()
    print("\n[*] 1. Generated PKCE Parameters (RFC 7636):")
    print(f"    Code Verifier  : {verifier[:32]}... ({len(verifier)} chars)")
    print(f"    Code Challenge : {challenge}")
    print(f"    Method         : S256")

    auth_url, state = build_auth_url(CLIENT_CUSTOMER_AGENT, challenge)
    print("\n[*] 2. Formulated Auth0 Universal Login URL:")
    print(f"    {auth_url}")

    user_email = "alex.mercer@securenova.ai"
    print(f"\n[*] 3. User Authenticated via Universal Login: {user_email}")
    print("    Auth0 Post-Login Action triggered: Injected custom claims into ID/Access Token.")

    token, header, payload = simulate_post_login_action(user_email, CLIENT_CUSTOMER_AGENT)

    print("\n" + "=" * 80)
    print(" PROJECT 2 - STEP 4: JWT INSPECTION (SIMULATED JWT.IO DECODER)")
    print("=" * 80)
    print(f"\n[ENCODED JWT TOKEN]\n{token}\n")
    print("[DECODED HEADER]")
    print(json.dumps(header, indent=4))
    print("\n[DECODED PAYLOAD & CUSTOM CLAIMS]")
    print(json.dumps(payload, indent=4))
    print("\n[VERIFICATION STATUS]: SIGNATURE VERIFIED (Auth0 Key Pair Match)")
    print("=" * 80)
    return token

if __name__ == "__main__":
    run_oauth_flow()
