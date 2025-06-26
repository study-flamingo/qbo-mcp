"""Minimal authentication wrapper using intuit-oauth package."""

import json
import logging
import webbrowser
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import parse_qs, urlparse
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError
from quickbooks import QuickBooks

from .config import config

logger = logging.getLogger("qbo_mcp")



class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback."""
    
    def do_GET(self):
        """Handle GET request for OAuth callback."""
        if self.path.startswith('/callback'):
            CallbackHandler.callback_url = f"http://localhost:8080{self.path}"
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            success_html = """
            <html><body>
                <h2>✅ QuickBooks Authentication Successful!</h2>
                <p>You can close this window.</p>
                <script>window.close();</script>
            </body></html>
            """
            self.wfile.write(success_html.encode())
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        """Suppress HTTP server logging."""
        pass


class QBOAuthManager:
    """Minimal auth manager using intuit-oauth package."""
    
    def __init__(self, token_file: Path | None = None):
        """Initialize auth manager."""
        self.token_file = token_file or config.token_file
        self.auth_client = AuthClient(
            client_id=config.client_id,
            client_secret=config.client_secret,
            redirect_uri=config.redirect_uri,
            environment=config.environment
        )
        self._load_tokens()
    
    def _load_tokens(self) -> None:
        """Load tokens from disk into AuthClient."""
        if not self.token_file.exists():
            return
        
        try:
            with open(self.token_file, 'r') as f:
                tokens = json.load(f)
            
            # Set tokens directly on AuthClient - let it handle the rest
            self.auth_client.access_token = tokens.get('access_token')
            self.auth_client.refresh_token = tokens.get('refresh_token')
            self.auth_client.realm_id = tokens.get('realm_id')
            
            logger.info(f"Loaded tokens from {self.token_file}")
            
        except Exception as e:
            logger.error(f"Error loading tokens: {e}")
    
    def _save_tokens(self) -> None:
        """Save AuthClient tokens to disk."""
        try:
            tokens = {
                'access_token': self.auth_client.access_token,
                'refresh_token': self.auth_client.refresh_token,
                'realm_id': self.auth_client.realm_id,
                'saved_at': time.time()
            }
            
            self.token_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.token_file, 'w') as f:
                json.dump(tokens, f, indent=2)
            
            logger.info(f"Saved tokens to {self.token_file}")
            
        except Exception as e:
            logger.error(f"Error saving tokens: {e}")
    
    def _perform_oauth_flow(self) -> bool:
        """Perform OAuth flow using intuit-oauth."""
        try:
            # Start callback server
            server = HTTPServer(('localhost', 8080), CallbackHandler)
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            # Get auth URL from intuit-oauth
            auth_url = self.auth_client.get_authorization_url([Scopes.ACCOUNTING])
            
            print("\n🔐 Opening browser for QuickBooks authorization...")
            webbrowser.open(auth_url)
            
            # Wait for callback
            CallbackHandler.callback_url = None
            timeout = 300  # 5 minutes
            start_time = time.time()
            
            while CallbackHandler.callback_url is None:
                if time.time() - start_time > timeout:
                    logger.error("OAuth timeout")
                    return False
                time.sleep(1)
            
            # Process callback
            parsed_url = urlparse(CallbackHandler.callback_url)
            query_params = parse_qs(parsed_url.query)
            
            if 'error' in query_params:
                logger.error(f"OAuth error: {query_params['error'][0]}")
                return False
            
            auth_code = query_params.get('code', [None])[0]
            realm_id = query_params.get('realmId', [None])[0]
            
            if not auth_code or not realm_id:
                logger.error("Missing auth code or realm ID")
                return False
            
            # Let intuit-oauth handle token exchange
            self.auth_client.get_bearer_token(auth_code, realm_id=realm_id)
            
            # Save the tokens AuthClient received
            self._save_tokens()
            
            logger.info(f"✅ Authenticated with QuickBooks (Company: {realm_id})")
            return True
            
        except AuthClientError as e:
            logger.error(f"OAuth error: {e.status_code} - {e.content}")
            return False
        except Exception as e:
            logger.error(f"OAuth flow error: {e}")
            return False
        finally:
            server.shutdown()
    
    def ensure_authenticated(self) -> bool:
        """Ensure we have valid authentication."""
        # Check if we have tokens
        if not self.auth_client.access_token:
            logger.info("No access token, starting OAuth flow...")
            return self._perform_oauth_flow()
        
        # Try to refresh if we have refresh token
        if self.auth_client.refresh_token:
            try:
                self.auth_client.refresh()  # Let intuit-oauth handle refresh
                self._save_tokens()  # Save updated tokens
                logger.info("✅ Refreshed tokens")
                return True
            except AuthClientError as e:
                logger.info(f"Refresh failed ({e.status_code}), starting new OAuth...")
                return self._perform_oauth_flow()
        
        # No refresh token, start new OAuth
        logger.info("No refresh token, starting OAuth flow...")
        return self._perform_oauth_flow()
    
    def get_authenticated_client(self) -> Optional[QuickBooks]:
        """Get authenticated QuickBooks client."""
        if not self.ensure_authenticated():
            return None
        
        if not self.auth_client.access_token or not self.auth_client.realm_id:
            logger.error("Missing tokens after authentication")
            return None
        
        try:
            return QuickBooks(
                access_token=self.auth_client.access_token,
                company_id=self.auth_client.realm_id,
                environment=config.environment
            )
        except Exception as e:
            logger.error(f"Error creating QuickBooks client: {e}")
            return None
    
    def revoke_tokens(self) -> bool:
        """Revoke tokens using intuit-oauth."""
        try:
            if self.auth_client.refresh_token:
                self.auth_client.revoke()  # Let intuit-oauth handle revocation
                
                # Clear saved tokens
                if self.token_file.exists():
                    self.token_file.unlink()
                
                logger.info("✅ Revoked tokens")
                return True
            return False
        except AuthClientError as e:
            logger.error(f"Revoke error: {e.status_code} - {e.content}")
            return False
    
    @property
    def is_authenticated(self) -> bool:
        """Check if authenticated."""
        return bool(self.auth_client.access_token and self.auth_client.realm_id)
    
    def get_company_info(self) -> dict[str, Any] | None:
        """Get company info."""
        if not self.is_authenticated:
            return {
                "error": "Not authenticated"
            }
        
        return {
            "company_id": self.auth_client.realm_id,
            "environment": config.environment,
            "has_access_token": bool(self.auth_client.access_token),
            "has_refresh_token": bool(self.auth_client.refresh_token)
        }


# Global authenticator instance
authenticator = QBOAuthManager()
