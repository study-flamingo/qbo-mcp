import logging
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)


def run_interactive_oauth(auth_client, scopes):
    """
    Run the interactive OAuth flow: start a local server, open browser, capture code/realmId, exchange for tokens.
    Returns a dict: {access_token, refresh_token, environment, realm_id}
    """
    class OAuthHandler(BaseHTTPRequestHandler):
        server_version = "OAuthHandler/0.1"
        code = None
        realm_id = None
        error = None
        def do_GET(self):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            if 'code' in params and 'realmId' in params and parsed.path == '/callback':
                OAuthHandler.code = params['code'][0]
                OAuthHandler.realm_id = params['realmId'][0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Authentication successful. You may close this window.</h1></body></html>")
            elif 'error' in params:
                OAuthHandler.error = params['error'][0]
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Authentication failed.</h1></body></html>")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Invalid request.</h1></body></html>")

    redirect_uri = auth_client.redirect_uri
    parsed_uri = urlparse(redirect_uri)
    host = parsed_uri.hostname or 'localhost'
    port = parsed_uri.port or 8000
    httpd = HTTPServer((host, port), OAuthHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info(f"Started local OAuth 2.0 server at http://{host}:{port}")

    try:
        auth_url = auth_client.get_authorization_url(scopes=scopes)
    except Exception as e:
        logger.error(f"Error getting authorization URL: {str(e)}")
        httpd.shutdown()
        server_thread.join()
        raise
    logger.info(f"\nPlease open the following URL in your browser to authorize the application:\n{auth_url}\n")
    webbrowser.open(auth_url, 2, True)
    logger.info("Waiting for user to complete OAuth flow...")

    while OAuthHandler.code is None and OAuthHandler.error is None:
        time.sleep(0.5)
    httpd.shutdown()
    server_thread.join()
    if OAuthHandler.error:
        logger.error(f"OAuth error: {OAuthHandler.error}")
        raise RuntimeError(f"OAuth error: {OAuthHandler.error}")
    if not OAuthHandler.code or not OAuthHandler.realm_id:
        logger.error("Did not receive code and realmId from OAuth redirect.")
        raise RuntimeError("Did not receive code and realmId from OAuth redirect.")
    try:
        auth_client.get_bearer_token(OAuthHandler.code, OAuthHandler.realm_id)
        tokens = {
            'access_token': auth_client.access_token,
            'refresh_token': auth_client.refresh_token,
            'environment': auth_client.environment,
            'realm_id': auth_client.realm_id,
        }
        logger.info("Successfully obtained tokens from OAuth flow.")
        return tokens
    except Exception as e:
        logger.error(f"Failed to exchange code for tokens: {str(e)}")
        raise 