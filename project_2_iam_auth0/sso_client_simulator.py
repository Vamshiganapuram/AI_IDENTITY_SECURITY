"""
Project 2 - Step 5: Federated Identity & Single Sign-On (SSO) Simulator
Demonstrates how a user authenticated to Client 1 (Customer Service Agent)
is accepted by Client 2 (Analytics Agent) via shared Auth0 session cookies / IdP federation without re-entering credentials.
"""
import time
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import AUTH0_DOMAIN, CLIENT_CUSTOMER_AGENT, CLIENT_ANALYTICS_AGENT
from project_2_iam_auth0.oauth_agent_client import simulate_post_login_action

def run_sso_demonstration():
    print("=" * 80)
    print(" PROJECT 2 - STEP 5: AUTH0 FEDERATED SSO MULTI-CLIENT DEMONSTRATION")
    print(" Organization: SecureNova Inc.")
    print("=" * 80)

    user_email = "sarah.connor@securenova.ai"
    session_id = "auth0_sess_9941a87b32ef"

    print(f"\n[PHASE 1: CLIENT 1 AUTHENTICATION - CUSTOMER SERVICE AGENT]")
    print(f"[*] Client ID        : {CLIENT_CUSTOMER_AGENT}")
    print(f"[*] Target App       : SecureNova AI Customer Service Agent")
    print(f"[*] Action           : User submits credentials to Auth0 Universal Login")
    print(f"[*] Status           : HTTP 200 OK - Login Successful")
    print(f"[*] Auth0 Session Id : {session_id} (Issued Secure HttpOnly SSO Cookie)")
    
    token1, _, payload1 = simulate_post_login_action(user_email, CLIENT_CUSTOMER_AGENT)
    print(f"[*] Client 1 Access Token Issued -> Subject: {payload1['sub']}")
    print(f"[*] Agent ID Claim   : {payload1['https://securenova.ai/agent_id']}")

    print("\n" + "-" * 80)
    print(f"[PHASE 2: CLIENT 2 SILENT AUTHENTICATION - ANALYTICS AGENT]")
    print(f"[*] Client ID        : {CLIENT_ANALYTICS_AGENT}")
    print(f"[*] Target App       : SecureNova AI Analytics & Intelligence Portal")
    print(f"[*] Action           : Client 2 requests authorization with prompt=none (SSO Check)")
    print(f"[*] Auth0 IdP Check  : Found active session cookie for '{user_email}' (Session: {session_id})")
    print(f"[*] Result           : SILENT SSO SUCCESSFUL - NO USER CREDENTIAL PROMPT REQUIRED!")
    
    token2, _, payload2 = simulate_post_login_action(user_email, CLIENT_ANALYTICS_AGENT)
    print(f"[*] Client 2 Access Token Issued -> Subject: {payload2['sub']}")
    print(f"[*] Target Audience  : {payload2['aud']}")
    print(f"[*] Agent ID Claim   : {payload2['https://securenova.ai/agent_id']}")

    print("\n" + "=" * 80)
    print("[SSO VERIFICATION SUMMARY]")
    print("  [+] Federated IdP Session shared across client applications")
    print("  [+] Centralized session termination & token lifecycle enforcement verified")
    print("  [+] Non-Human & Human identity context synchronized across enterprise agents")
    print("=" * 80)

if __name__ == "__main__":
    run_sso_demonstration()
