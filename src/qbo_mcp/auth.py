"""Minimal authentication wrapper using intuit-oauth package."""

import json
import logging
import os
from pathlib import Path
from typing import Any

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from quickbooks import QuickBooks

from qbo_mcp.config import QBOConfig, config

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class QBOService:
    """
    Manages QuickBooks Online (QBO) authentication, token management, and client creation.

    This service wraps the intuit-oauth AuthClient and provides methods to ensure valid authentication,
    handle token persistence, and return authenticated QuickBooks client instances for API access.
    """
    
    def __init__(self, config: QBOConfig):
        """
        Initialize the QBOService with configuration and load any existing tokens.

        Args:
            config (QBOConfig): Configuration object containing credentials and file paths.
        """
        self.token_file = config.token_file
        self.auth_client = AuthClient(
            client_id=config.client_id,
            client_secret=config.client_secret,
            redirect_uri=config.redirect_uri,
            environment=config.environment,
        )
        self._load_tokens()
        self.qbo: QuickBooks
        logger.info("QBOService initialized!")

    def _load_tokens(self) -> None:
        """
        Load tokens from disk or environment variables and set them on the AuthClient.

        Tries to load from the configured token file first. If not found, falls back to environment variables.
        If both fail, assumes authentication has not been run and initiates a new auth session.
        """
        import threading
        from http.server import BaseHTTPRequestHandler, HTTPServer
        from urllib.parse import urlparse, parse_qs

        tokens = {}
        # 1. Try loading from token file
        try:
            with open(self.token_file, 'r') as f:
                tokens = json.load(f)
            logger.info(f"Loaded tokens from {self.token_file}")
        except FileNotFoundError:
            logger.warning(f"Token file not found at {self.token_file}")
        except Exception as e:
            logger.warning(f"Error reading token file: {str(e)}")

        # 2. If file failed, try environment
        if not tokens.get('access_token'):
            env_tokens = {
                "access_token": os.getenv("QBO_ACCESS_TOKEN"),
                "refresh_token": os.getenv("QBO_REFRESH_TOKEN"),
                "environment": os.getenv("QBO_ENVIRONMENT", "sandbox")
            }
            env_tokens = {k: v for k, v in env_tokens.items() if v is not None}
            if env_tokens.get('access_token'):
                tokens = env_tokens
                logger.info("Loaded tokens from environment variables.")
            else:
                logger.warning("No tokens found in environment variables.")

        # 3. If neither file nor env provided tokens, start new auth session
        if not tokens.get('access_token'):
            logger.warning("No tokens found in file or environment. Starting new authentication session.")
            # Minimal local HTTP server to capture redirect
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

            # Start server in a thread
            redirect_uri = self.auth_client.redirect_uri
            parsed_uri = urlparse(redirect_uri)
            host = parsed_uri.hostname or 'localhost'
            port = parsed_uri.port or 8000
            httpd = HTTPServer((host, port), OAuthHandler)
            server_thread = threading.Thread(target=httpd.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            logger.info(f"Started local OAuth 2.0 server at http://{host}:{port}")

            # Set scopes
            scopes: list[Scopes] = [Scopes.ACCOUNTING]
            
            # Print auth URL for user
            try:
                auth_url = self.auth_client.get_authorization_url(scopes=scopes)
            except Exception as e:
                logger.error(f"Error getting authorization URL: {str(e)}")
                raise
            logger.info(f"\nPlease open the following URL in your browser to authorize the application:\n{auth_url}\n")
            import webbrowser
            webbrowser.open(auth_url, 2, True)
            logger.info("Waiting for user to complete OAuth flow...")

            # Wait for code/realmId
            import time
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
            # Exchange code for tokens
            try:
                self.auth_client.get_bearer_token(OAuthHandler.code, OAuthHandler.realm_id)
                tokens = {
                    'access_token': self.auth_client.access_token,
                    'refresh_token': self.auth_client.refresh_token,
                    'environment': self.auth_client.environment,
                }
                print(tokens)
                self._save_tokens()
                logger.info("Successfully obtained and saved tokens from initial OAuth flow.")
            except Exception as e:
                logger.error(f"Failed to exchange code for tokens: {str(e)}")
                raise

        # Set tokens on auth_client
        self.auth_client.access_token = tokens.get('access_token')
        self.auth_client.refresh_token = tokens.get('refresh_token')
        env = tokens.get('environment')
        self.auth_client.environment = env if env is not None else 'sandbox'

    def _save_tokens(self) -> None:
        """
        Persist the current AuthClient tokens to disk.

        Saves the access token, refresh token, and environment string to the configured token file.
        """
        try:
            tokens = {
                'access_token': self.auth_client.access_token,
                'refresh_token': self.auth_client.refresh_token,
                'environment': self.auth_client.environment,
            }
            self.token_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.token_file, 'w') as f:
                json.dump(tokens, f, indent=2)
            logger.info(f"💾  Saved tokens to {self.token_file}")
        except Exception as e:
            logger.error(f"Error saving tokens: {str(e)}")

    def ensure_authenticated(self) -> bool:
        """
        Ensure valid authentication by refreshing tokens if necessary.

        Attempts to refresh the access token using the refresh token. Saves new tokens to disk if successful.
        Raises an error if no refresh token is available or if the refresh fails.

        Returns:
            bool: True if tokens were refreshed successfully.
        """
        if not self.auth_client:
            raise ValueError("Auth client not initialized!")
        if not self.auth_client.refresh_token:
            raise ValueError("No refresh token found!")
        try:
            self.auth_client.refresh()
            self._save_tokens()
            logger.info("Tokens refreshed successfully!")
            return True
        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            return False

    def get_authenticated_client(self) -> QuickBooks:
        """
        Return an authenticated QuickBooks client, ensuring valid tokens.

        Calls ensure_authenticated() to refresh tokens if needed, then returns a QuickBooks client
        configured with the current AuthClient and environment.

        Returns:
            QuickBooks: An authenticated QuickBooks client instance.
        Raises:
            ValueError: If authentication fails or required tokens are missing.
        """
        if not self.ensure_authenticated():
                try:
                    self.qbo = QuickBooks(
                        auth_client=self.auth_client,
                        refresh_token=self.auth_client.refresh_token,
                        company_id=self.auth_client.environment,
                    )
                except Exception as e:
                    raise ValueError(f"QBO Service error: {str(e)}")
        return self.qbo

    def revoke_tokens(self) -> bool:
        """
        Revoke the current refresh token and clear persisted tokens.

        Uses the AuthClient to revoke the refresh token, then deletes the token file if it exists.

        Returns:
            bool: True if tokens were revoked, False if no refresh token was present.
        Raises:
            ValueError: If revocation fails.
        """
        try:
            if self.auth_client.refresh_token:
                self.auth_client.revoke()
                if self.token_file.exists():
                    self.token_file.unlink()
                logger.info("✅ Revoked tokens")
                return True
            return False
        except Exception as e:
            raise ValueError(f"Revocation error: {str(e)}")

    def get_company_info(self) -> dict[str, Any] | None:
        """
        Get basic company/environment info for the current authentication context.

        Returns:
            dict[str, Any] | None: Dictionary with company/environment info, or error if not authenticated.
        """
        if not self.ensure_authenticated():
            return {
                "error": "Not authenticated"
            }
        return {
            "company_id": self.auth_client.environment,
            "environment": config.environment,
            "has_access_token": bool(self.auth_client.access_token),
            "has_refresh_token": bool(self.auth_client.refresh_token)
        }


# Global authenticator instance
qbo_service = QBOService(config=config)

__all__ = ["qbo_service"]