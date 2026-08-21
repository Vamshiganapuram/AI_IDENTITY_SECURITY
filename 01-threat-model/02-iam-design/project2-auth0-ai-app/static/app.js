const output = document.getElementById("output");
const statusEl = document.getElementById("status");

function show(obj) {
  output.textContent = typeof obj === "string" ? obj : JSON.stringify(obj, null, 2);
}

async function createClient() {
  const cfg = window.SECURENOVA_CONFIG;
  return await auth0.createAuth0Client({
    domain: cfg.domain,
    clientId: cfg.clientId,
    authorizationParams: {
      redirect_uri: cfg.redirectUri,
      audience: cfg.audience,
      scope: cfg.scopes,
    },
    cacheLocation: "localstorage",
    useRefreshTokens: true,
  });
}

async function main() {
  const client = await createClient();

  if (window.location.search.includes("code=") && window.location.search.includes("state=")) {
    await client.handleRedirectCallback();
    window.history.replaceState({}, document.title, "/");
  }

  const loggedIn = await client.isAuthenticated();
  document.getElementById("login").onclick = () =>
    client.loginWithRedirect({
      authorizationParams: {
        audience: window.SECURENOVA_CONFIG.audience,
        scope: window.SECURENOVA_CONFIG.scopes,
      },
    });
  document.getElementById("logout").onclick = () =>
    client.logout({ logoutParams: { returnTo: window.SECURENOVA_CONFIG.redirectUri } });

  document.getElementById("logout").hidden = !loggedIn;
  document.getElementById("call-chat").disabled = !loggedIn;
  document.getElementById("call-admin").disabled = !loggedIn;
  document.getElementById("show-token").disabled = !loggedIn;

  if (!loggedIn) {
    statusEl.textContent = "Not signed in. Use Log in (PKCE).";
    return;
  }

  const user = await client.getUser();
  statusEl.textContent = `Signed in as ${user.email || user.sub} (agent_id=${user.agent_id || "see ID token at jwt.io"})`;

  async function call(path) {
    const token = await client.getTokenSilently();
    const res = await fetch(path, { headers: { Authorization: `Bearer ${token}` } });
    const text = await res.text();
    let body;
    try {
      body = JSON.parse(text);
    } catch {
      body = text;
    }
    show({ path, status: res.status, statusText: res.statusText, body });
  }

  document.getElementById("call-chat").onclick = () => call("/chat");
  document.getElementById("call-admin").onclick = () => call("/admin");
  document.getElementById("show-token").onclick = async () => {
    const accessToken = await client.getTokenSilently();
    const idClaims = await client.getIdTokenClaims();
    const idToken = idClaims.__raw;
    show(
      "1) Open https://jwt.io\n" +
        "2) Paste ACCESS TOKEN first (must show aud, iss, exp, scope).\n" +
        "3) Paste ID TOKEN second (must show agent_id).\n\n" +
        "===== ACCESS TOKEN =====\n" +
        accessToken +
        "\n\n===== ID TOKEN =====\n" +
        idToken
    );
  };
}

main().catch((err) => {
  statusEl.textContent = "Auth0 client failed to start. Check AUTH0_DOMAIN and SPA client ID.";
  show(String(err));
});
