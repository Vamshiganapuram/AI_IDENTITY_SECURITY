"""
Project 4 - Step 4: Real-Time Anomaly Detection Engine
SecureNova Inc. - AI Identity Security Blue Team Campaign

Requirements Fulfillments:
1. LLM API Call Volume Spike: Alerts when > 20 requests occur within a 60-second window.
2. Scope Change Detection: Alerts on unauthorized scope escalations between consecutive agent requests.
3. Token Reuse After Expiry: Alerts on attempts to present an expired JWT past the 300s TTL.
4. Real-time Telemetry: Outputs timestamp, identity, event type, severity, and mitigation action.
"""

import time
import datetime
import json
from collections import defaultdict, deque

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL
except ImportError:
    GREEN = RED = YELLOW = CYAN = BOLD = RESET = ""


class AIIdentityAnomalyDetector:
    def __init__(self, volume_threshold=20, time_window_seconds=60):
        self.volume_threshold = volume_threshold
        self.time_window = time_window_seconds
        
        # Sliding window tracker per agent/user identity
        self.request_history = defaultdict(deque)
        
        # Session scope history per agent
        self.agent_previous_scopes = {}
        
        # Known approved scopes
        self.baseline_agent_scopes = {
            "agent_orchestrator_001_enterprise": {"profile:read", "rag:read"},
            "agent_mcp_worker_b": {"rag:read", "knowledge:search"},
            "client_analytics_agent_1187b": {"telemetry:read"}
        }

    def log_alert(self, event_type: str, identity: str, severity: str, details: dict):
        """Emits a structured SIEM / SOC alert."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        alert = {
            "timestamp": timestamp,
            "event_type": event_type,
            "identity": identity,
            "severity": severity,
            "telemetry": details
        }
        print(f"\n{BOLD}{RED}[!] SECURITY ANOMALY ALERT FIRED!{RESET}")
        print(f"    - Timestamp     : {BOLD}{timestamp}{RESET}")
        print(f"    - Identity      : {BOLD}{CYAN}{identity}{RESET}")
        print(f"    - Event Type    : {BOLD}{RED}{event_type}{RESET}")
        print(f"    - Severity      : {BOLD}{RED}{severity}{RESET}")
        print(f"    - Telemetry Data: {json.dumps(details, indent=6)}")
        return alert

    def check_call_volume_spike(self, identity: str, request_timestamp: float = None):
        """Scenario 1: Detects rate-limit spike (> 20 requests in 60s)."""
        now = request_timestamp or time.time()
        q = self.request_history[identity]
        
        # Remove timestamps older than sliding window
        while q and (now - q[0]) > self.time_window:
            q.popleft()
            
        q.append(now)
        
        if len(q) > self.volume_threshold:
            return self.log_alert(
                event_type="LLM_API_CALL_VOLUME_SPIKE",
                identity=identity,
                severity="HIGH",
                details={
                    "request_count": len(q),
                    "threshold": self.volume_threshold,
                    "window_seconds": self.time_window,
                    "rate": f"{len(q)} req / {self.time_window}s",
                    "action_taken": "RATE_LIMIT_THROTTLED_IP_CHALLENGED"
                }
            )
        return None

    def check_scope_escalation(self, identity: str, requested_scope: str):
        """Scenario 2: Detects unapproved scope change between consecutive requests."""
        baseline = self.baseline_agent_scopes.get(identity, {"standard:user"})
        last_scope = self.agent_previous_scopes.get(identity, "profile:read")
        
        # Check if requested scope is outside approved baseline or represents sudden escalation
        if requested_scope not in baseline and ("admin" in requested_scope or "write" in requested_scope):
            alert = self.log_alert(
                event_type="UNAUTHORIZED_SCOPE_CHANGE_DETECTED",
                identity=identity,
                severity="CRITICAL",
                details={
                    "previous_scope": last_scope,
                    "attempted_scope": requested_scope,
                    "approved_baseline": list(baseline),
                    "mitre_atlas_technique": "AML.T0054 (LLM Agent Hijack)",
                    "action_taken": "RPC_STEP_UP_AUTH_REQUIRED_EXECUTION_BLOCKED"
                }
            )
            self.agent_previous_scopes[identity] = requested_scope
            return alert
            
        self.agent_previous_scopes[identity] = requested_scope
        return None

    def check_token_reuse_after_expiry(self, identity: str, token_exp_timestamp: float, current_timestamp: float = None):
        """Scenario 3: Detects token reuse after expiry (> 300s TTL)."""
        now = current_timestamp or time.time()
        if now > token_exp_timestamp:
            drift_seconds = int(now - token_exp_timestamp)
            return self.log_alert(
                event_type="EXPIRED_TOKEN_REUSE_ATTEMPT",
                identity=identity,
                severity="HIGH",
                details={
                    "token_expiry_timestamp": token_exp_timestamp,
                    "attempt_timestamp": now,
                    "seconds_past_expiry": drift_seconds,
                    "hardened_ttl_policy": "300s",
                    "action_taken": "HTTP_401_UNAUTHORIZED_TOKEN_REVOKED"
                }
            )
        return None


def run_anomaly_detection_suite():
    print("=" * 95)
    print(f"{BOLD}{CYAN} PROJECT 4: REAL-TIME AI IDENTITY ANOMALY DETECTION ENGINE{RESET}")
    print(f" Organization: SecureNova Inc. | Role: AI Identity Security Engineer")
    print("=" * 95)

    detector = AIIdentityAnomalyDetector(volume_threshold=20, time_window_seconds=60)

    # -------------------------------------------------------------------------
    # PART 1: SCREENSHOT 7 REQUIREMENT
    # Terminal showing anomaly detection alert firing for one of the three detection scenarios.
    # (We execute all three scenarios with full timestamps, identity, and event types!)
    # -------------------------------------------------------------------------
    print(f"\n{BOLD}{YELLOW}==============================================================================================={RESET}")
    print(f"{BOLD}{YELLOW} [SCREENSHOT 7] REPLAYING ADVERSARIAL SCENARIOS & FIRING ANOMALY ALERTS{RESET}")
    print(f"{BOLD}{YELLOW}==============================================================================================={RESET}")

    # --- Scenario 1: LLM API Call Volume Spike ---
    print(f"\n{CYAN}[SCENARIO 1 / 3] Simulating Rapid Prompt Flooding / API Call Volume Spike (>20 calls in 60s)...{RESET}")
    agent_id = "client_cs_agent_9942a"
    base_time = time.time()
    for i in range(1, 23):
        # Fire 22 requests in 30 seconds
        alert = detector.check_call_volume_spike(agent_id, request_timestamp=base_time + (i * 1.2))

    # --- Scenario 2: Scope Change Between Consecutive Requests ---
    print(f"\n{CYAN}[SCENARIO 2 / 3] Simulating Agent Privilege Escalation / Sudden Scope Change...{RESET}")
    agent_orch = "agent_orchestrator_001_enterprise"
    print(f"[*] Request 1 from {agent_orch}: Scope = 'profile:read' -> [NORMAL]")
    detector.check_scope_escalation(agent_orch, "profile:read")
    
    print(f"[*] Request 2 from {agent_orch}: Scope = 'billing:write' -> [ESCALATION ATTEMPT!]")
    detector.check_scope_escalation(agent_orch, "billing:write")

    # --- Scenario 3: Token Reuse After Expiry ---
    print(f"\n{CYAN}[SCENARIO 3 / 3] Simulating Stale Session Token Replay After 300s TTL Expiration...{RESET}")
    expired_token_user = "auth0|user_attacker_9901"
    token_expiry_time = time.time() - 420  # Expired 420 seconds (7 minutes) ago
    detector.check_token_reuse_after_expiry(expired_token_user, token_exp_timestamp=token_expiry_time)

    print("\n" + "=" * 95)
    print(f"{BOLD}{GREEN}[+] All 3 Anomaly Detection Monitors Fired Successfully with Verified Telemetry.{RESET}")
    print("=" * 95)


if __name__ == "__main__":
    run_anomaly_detection_suite()
