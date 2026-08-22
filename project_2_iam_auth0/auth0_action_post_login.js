/**
 * Auth0 Post-Login Action: AI Identity & Agent Context Claim Injection
 * Organization: SecureNova Inc.
 * 
 * Purpose:
 * Injects non-human identity claims (agent_id, trust_tier, session_fingerprint)
 * into both ID Tokens and Access Tokens to enforce Zero-Trust access control
 * across downstream LLM agents, RAG pipelines, and MCP server gateways.
 * 
 * @param {Event} event - Details about the user and the context of the authentication transaction.
 * @param {ActionAPI} api - Interface and methods to change the behavior of the login flow.
 */
exports.onExecutePostLogin = async (event, api) => {
  const namespace = 'https://securenova.ai/';
  
  // 1. Determine Identity Role and Assign Autonomous Agent Identifier
  let assignedAgentId = 'agent_cs_9942a';
  let trustTier = 'Tier-2_Autonomous';
  
  if (event.user.email && event.user.email.endsWith('@securenova.ai')) {
    assignedAgentId = 'agent_orchestrator_001_enterprise';
    trustTier = 'Tier-1_Privileged';
  }

  // 2. Set Custom Claims in ID Token (for Client UI context)
  api.idToken.setCustomClaim(`${namespace}agent_id`, assignedAgentId);
  api.idToken.setCustomClaim(`${namespace}trust_tier`, trustTier);
  api.idToken.setCustomClaim(`${namespace}assigned_tenant`, 'ten_securenova_enterprise_01');
  api.idToken.setCustomClaim(`${namespace}session_risk_score`, 0.05);

  // 3. Set Custom Claims in Access Token (for Internal APIs & MCP Gateway validation)
  api.accessToken.setCustomClaim(`${namespace}agent_id`, assignedAgentId);
  api.accessToken.setCustomClaim(`${namespace}trust_tier`, trustTier);
  api.accessToken.setCustomClaim(`${namespace}allowed_tools`, [
    'rag:query_knowledge_base',
    'profile:lookup_customer_profile'
  ]);
  
  // 4. Audit Log Emission
  console.log(`[AUTH0 ACTION] Injected agent identity claims for user: ${event.user.email} -> Assigned Agent: ${assignedAgentId} (${trustTier})`);
};
