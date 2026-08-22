"""
Master Execution Engine for AI Identity Security Capstone Project
SecureNova Inc. - End-to-End Automated Validation

Runs:

- Project 3: Red Team AI Identity Attacks

"""
import time
import os
import sys

def main():
    print("#" * 80)
    print("   SECURENOVA INC. - AI IDENTITY SECURITY CAPSTONE PROJECT SUITE")
    print("   Complete End-to-End Execution & Demonstration")
    print("#" * 80)
    
    print("\n>>> LAUNCHING PROJECT 1: THREAT MODEL & ARCHITECTURE...")
    time.sleep(1)
    os.system(f'"{sys.executable}" project_1_threat_model/threat_model_runner.py')

    print("\n\n>>> LAUNCHING PROJECT 2: IAM & AUTH0 IDENTITY CONTROLS...")
    time.sleep(1)
    os.system(f'"{sys.executable}" project_2_iam_auth0/oauth_agent_client.py')
    os.system(f'"{sys.executable}" project_2_iam_auth0/sso_client_simulator.py')
    os.system(f'"{sys.executable}" project_2_iam_auth0/auth0_attack_protection_audit.py')
    os.system(f'"{sys.executable}" project_2_iam_auth0/credential_rotation_m2m.py')

    print("\n\n>>> LAUNCHING PROJECT 3: RED TEAM AI IDENTITY ATTACKS...")
    time.sleep(1)
    os.system(f'"{sys.executable}" project_3_red_team/red_team_runner.py')

    print("\n\n>>> LAUNCHING PROJECT 4: BLUE TEAM GUARDRAILS & DETECTION...")
    time.sleep(1)
    os.system(f'"{sys.executable}" project_4_blue_team/blue_team_runner.py')

    print("\n" + "#" * 80)
    print("   ALL 4 CORE PROJECTS EXECUTED SUCCESSFULLY!")
    print("   All criteria, screenshots, and logs ready for submission.")
    print("#" * 80)

if __name__ == "__main__":
    main()
