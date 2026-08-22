/**
 * Auth0 Action — Login / Post Login
 * Trigger: Post Login
 * Runtime: Node 18+
 *
 * Adds a custom claim `agent_id` to the ID token (and access token)
 * so jwt.io can show it for Project 2 screenshot 3.
 */
exports.onExecutePostLogin = async (event, api) => {
  const namespace = "";
  const agentId = `sn-agent-${event.user.user_id}`;

  api.idToken.setCustomClaim(`${namespace}agent_id`, agentId);
  api.accessToken.setCustomClaim(`${namespace}agent_id`, agentId);
};
