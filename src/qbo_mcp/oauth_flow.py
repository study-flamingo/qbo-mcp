"""Interactive OAuth 2.0 flow for QuickBooks Online.

Runs a short-lived local callback server, opens the browser, and exchanges the
authorization code for tokens. The OAuth ``state`` parameter is generated and
verified on callback to protect against CSRF, and the wait is bounded by a
timeout so a headless/locked-down environment cannot hang forever.
"""

import logging
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

# How long to wait for the user to complete the browser handshake.
_OAUTH_TIMEOUT_SECONDS = 300


def run_interactive_oauth(auth_client, scopes):
    """
    Run the interactive OAuth flow: start a local server, open the browser,
    capture code/realmId/state, verify state, and exchange for tokens.

    Returns a dict: {access_token, refresh_token, environment, realm_id}
    """
    expected_state = secrets.token_urlsafe(24)

    class OAuthHandler(BaseHTTPRequestHandler):
        server_version = "OAuthHandler/0.2"
        code = None
        realm_id = None
        error = None
        state = None

        def log_message(self, *args):  # keep the stdio MCP transport clean
            return

        def _respond(self, status, message):
            self.send_response(status)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                f"<html><body><h1>{message}</h1></body></html>".encode()
            )

        def do_GET(self):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            if parsed.path == "/callback" and "code" in params and "realmId" in params:
                OAuthHandler.code = params["code"][0]
                OAuthHandler.realm_id = params["realmId"][0]
                OAuthHandler.state = (params.get("state") or [None])[0]
                self._respond(200, "Authentication successful. You may close this window.")
            elif "error" in params:
                OAuthHandler.error = params["error"][0]
                self._respond(400, "Authentication failed.")
            else:
                self._respond(400, "Invalid request.")

    redirect_uri = auth_client.redirect_uri
    parsed_uri = urlparse(redirect_uri)
    host = parsed_uri.hostname or "localhost"
    port = parsed_uri.port or 8000
    httpd = HTTPServer((host, port), OAuthHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info(f"Started local OAuth 2.0 server at http://{host}:{port}")

    try:
        auth_url = auth_client.get_authorization_url(scopes=scopes, state_token=expected_state)
    except Exception as e:
        logger.error(f"Error getting authorization URL: {str(e)}")
        httpd.shutdown()
        server_thread.join()
        raise
    logger.info(f"Please open the following URL in your browser to authorize:\n{auth_url}\n")
    webbrowser.open(auth_url, 2, True)
    logger.info("Waiting for user to complete OAuth flow...")

    deadline = time.time() + _OAUTH_TIMEOUT_SECONDS
    while OAuthHandler.code is None and OAuthHandler.error is None:
        if time.time() > deadline:
            httpd.shutdown()
            server_thread.join()
            raise RuntimeError("Timed out waiting for OAuth callback.")
        time.sleep(0.5)
    httpd.shutdown()
    server_thread.join()

    if OAuthHandler.error:
        logger.error(f"OAuth error: {OAuthHandler.error}")
        raise RuntimeError(f"OAuth error: {OAuthHandler.error}")
    if OAuthHandler.state != expected_state:
        logger.error("OAuth state mismatch; possible CSRF. Aborting.")
        raise RuntimeError("OAuth state mismatch; aborting authentication.")
    if not OAuthHandler.code or not OAuthHandler.realm_id:
        logger.error("Did not receive code and realmId from OAuth redirect.")
        raise RuntimeError("Did not receive code and realmId from OAuth redirect.")

    try:
        auth_client.get_bearer_token(OAuthHandler.code, OAuthHandler.realm_id)
        tokens = {
            "access_token": auth_client.access_token,
            "refresh_token": auth_client.refresh_token,
            "environment": auth_client.environment,
            "realm_id": auth_client.realm_id,
        }
        logger.info("Successfully obtained tokens from OAuth flow.")
        return tokens
    except Exception as e:
        logger.error(f"Failed to exchange code for tokens: {str(e)}")
        raise
