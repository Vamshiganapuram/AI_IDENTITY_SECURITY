"""
Central Configuration for SecureNova AI Identity Security Platform
"""
import os
import secrets

# Platform Configuration
PLATFORM_NAME = "SecureNova AI Customer Service Platform"
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "securenova-prod.us.auth0.com")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "https://api.securenova.ai/v1/")
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/"

# Client Application IDs
CLIENT_CUSTOMER_AGENT = "client_cs_agent_9942a"
CLIENT_ANALYTICS_AGENT = "client_analytics_agent_1187b"
CLIENT_MCP_GATEWAY = "client_mcp_gateway_5531c"

# JWT Mock Signing Key for offline verification
JWT_SECRET_KEY = secrets.token_hex(32)
MOCK_TENANT_ID = "ten_securenova_enterprise_01"

# Service Roles
ROLE_USER = "StandardUser"
ROLE_AGENT = "AutonomousAgent_Tier2"
ROLE_ADMIN = "SystemAdministrator"

# Target MCP tools
MCP_AVAILABLE_TOOLS = [
    {"name": "query_knowledge_base", "scope": "rag:read", "privileged": False},
    {"name": "lookup_customer_profile", "scope": "profile:read", "privileged": False},
    {"name": "issue_billing_refund", "scope": "billing:write", "privileged": True},
    {"name": "rotate_api_credentials", "scope": "admin:credentials", "privileged": True},
    {"name": "execute_database_query", "scope": "db:admin", "privileged": True}
]
