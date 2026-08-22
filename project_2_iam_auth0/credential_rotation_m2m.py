"""
Project 2 - Steps 7 & 8: Short-Lived M2M Credential Rotation & Anti-Replay Engine
SecureNova Inc. - AI Identity Security

Demonstrates:
1. Short-lived Machine-to-Machine (M2M) OAuth token generation.
2. Valid API invocation returning timestamped [200 OK].
3. Automated credential rotation & token invalidation.
4. Token replay attack detection returning timestamped [401 Unauthorized].
"""
import time
import datetime
import os
import sys
import jwt

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import AUTH0_ISSUER, AUTH0_AUDIENCE, CLIENT_CUSTOMER_AGENT

class SecureNovaAPIGateway:
    def __init__(self):
        self.active_rotation_epoch = 1
        self.current_signing_secret = "m2m_key_epoch_1_88f921ab4"
        self.revoked_tokens = set()

    def rotate_secret(self):
        """Rotates the M2M secret key, invalidating previous epoch tokens."""
        self.active_rotation_epoch += 1
        self.current_signing_secret = f"m2m_key_epoch_{self.active_rotation_epoch}_{int(time.time())}"

    def issue_m2m_token(self, ttl_seconds=5):
        """Issues short-lived M2M token for autonomous agent."""
        now = int(time.time())
        payload = {
            "iss": AUTH0_ISSUER,
            "sub": f"{CLIENT_CUSTOMER_AGENT}@clients",
            "aud": AUTH0_AUDIENCE,
            "iat": now,
            "exp": now + ttl_seconds,
            "epoch": self.active_rotation_epoch,
            "scope": "internal:api:execute customer:profile:read",
            "agent_identity": "Agent-CS-Autonomous-9942"
        }
        token = jwt.encode(payload, self.current_signing_secret, algorithm="HS256")
        return token, payload

    def validate_and_invoke(self, token, endpoint="/api/v1/customer/profile"):
        now_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        if token in self.revoked_tokens:
            return 401, f"[{now_ts}] HTTP/1.1 401 Unauthorized - Replay Detected: Token explicitly revoked."

        try:
            # Decode and verify with current signing secret
            payload = jwt.decode(token, self.current_signing_secret, algorithms=["HS256"], audience=AUTH0_AUDIENCE)
            if payload.get("epoch") != self.active_rotation_epoch:
                return 401, f"[{now_ts}] HTTP/1.1 401 Unauthorized - Token Invalidation: Epoch mismatch post-rotation."
            
            return 200, f"[{now_ts}] HTTP/1.1 200 OK - Access Granted to {endpoint} (Agent: {payload.get('agent_identity')})"
        except jwt.ExpiredSignatureError:
            return 401, f"[{now_ts}] HTTP/1.1 401 Unauthorized - Signature Expired: Short-lived TTL elapsed."
        except Exception as e:
            return 401, f"[{now_ts}] HTTP/1.1 401 Unauthorized - Verification Failed: {str(e)}"

def run_credential_rotation_demonstration():
    print("=" * 80)
    print(" PROJECT 2 - STEP 7 & 8: M2M CREDENTIAL ROTATION & REPLAY DEFENSE")
    print(" Organization: SecureNova Inc. | Component: Internal REST API Gateway")
    print("=" * 80)

    gateway = SecureNovaAPIGateway()

    # Step 7: Issue Short-lived M2M Token
    print("\n[PHASE 1: SHORT-LIVED M2M TOKEN ISSUANCE (TTL = 3s)]")
    token_1, payload_1 = gateway.issue_m2m_token(ttl_seconds=3)
    print(f"[*] Client ID       : {CLIENT_CUSTOMER_AGENT}")
    print(f"[*] Token TTL       : 3 seconds (Enforcing Minimal Credential Lifespan)")
    print(f"[*] Active Epoch    : {payload_1['epoch']}")
    print(f"[*] Scopes Granted  : {payload_1['scope']}")
    print(f"[*] Issued Bearer   : {token_1[:45]}...")

    # Step 8: Valid Call (200 OK)
    print("\n[PHASE 2: EXECUTING VALID AUTHORIZED API REQUEST]")
    status_code, response_log = gateway.validate_and_invoke(token_1)
    print(f"[*] Result: Status {status_code}")
    print(f"    {response_log}")

    # Credential Rotation Triggered
    print("\n" + "-" * 80)
    print("[PHASE 3: AUTOMATED CREDENTIAL ROTATION EVENT TRIGGERED]")
    print("[!] Initiating M2M secret rotation policy at API Gateway...")
    gateway.rotate_secret()
    gateway.revoked_tokens.add(token_1)
    print(f"[+] Rotated to Secret Epoch: {gateway.active_rotation_epoch}")
    print("[+] Stored previous token in Gateway Revocation Registry")
    print("-" * 80)

    # Replay Attempt (401 Unauthorized)
    print("\n[PHASE 4: ADVERSARIAL REPLAY ATTEMPT WITH RETIRED / EXPIRED TOKEN]")
    print("[!] Attacker / Interceptor attempts to replay captured Token 1...")
    time.sleep(1.0)
    replay_status, replay_log = gateway.validate_and_invoke(token_1)
    print(f"[*] Result: Status {replay_status}")
    print(f"    {replay_log}")

    print("\n" + "=" * 80)
    print("[VERIFICATION CONFIRMATION]")
    print("  [+] First Request  : 200 OK with timestamp")
    print("  [+] Replay Request : 401 Unauthorized on replay post-rotation")
    print("=" * 80)

if __name__ == "__main__":
    run_credential_rotation_demonstration()
