"""Enhanced authentication module with automatic auth handling."""

import json
import logging
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import parse_qs, urlparse
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from quickbooks import QuickBooks

from .config import config

logger = logging.getLogger(__name__)


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback."""
    
    def do_GET(self):
        """Handle GET request for OAuth callback."""
        if self.path.startswith('/callback'):
            # Store the callback URL for processing
            CallbackHandler.callback_url = f"http://localhost:8080{self.path}"
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            success_html = """
            <html>
            <body>
                <h2>Authentication Successful!</h2>
                <p>You can close this window and return to your application.</p>
                <script>window.close();</script>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode())
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        """Suppress default HTTP server logging."""
        pass


class QBOTokenManager:
    """Manages OAuth tokens for QuickBooks Online."""
    
    def __init__(self, token_file: Optional[Path] = None):
        """Initialize token manager with optional custom token file path."""
        self.token_file = token_file or config.token_file
        self._tokens: Dict[str, Any] = {}
        self._load_tokens()
    
    def _load_tokens(self) -> None:
        """Load tokens from file if it exists."""
        if self.token_file.exists():
            try:
                with open(self.token_file, 'r') as f:
                    self._tokens = json.load(f)
                logger.info(f"Loaded tokens from {self.token_file}")
            except Exception as e:
                logger.error(f"Error loading tokens: {e}")
                self._tokens = {}
    
    def _save_tokens(self) -> None:
        """Save tokens to file."""
        try:
            self.token_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.token_file, 'w') as f:
                json.dump(self._tokens, f, indent=2)
            logger.info(f"Saved tokens to {self.token_file}")
        except Exception as e:
            logger.error(f"Error saving tokens: {e}")
    
    def store_tokens(self, access_token: str, refresh_token: str, 
                    company_id: str, expires_in: int = 3600) -> None:
        """Store OAuth tokens."""
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        
        self._tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "company_id": company_id,
            "expires_at": expires_at.isoformat(),
            "created_at": datetime.now().isoformat()
        }
        self._save_tokens()
    
    def get_access_token(self) -> Optional[str]:
        """Get current access token if valid."""
        if not self._tokens:
            return None
            
        try:
            expires_at = datetime.fromisoformat(self._tokens.get("expires_at", ""))
            if datetime.now() >= expires_at:
                logger.info("Access token expired")
                return None
        except ValueError:
            logger.error("Invalid expires_at format")
            return None
            
        return self._tokens.get("access_token")
    
    def get_refresh_token(self) -> Optional[str]:
        """Get refresh token."""
        return self._tokens.get("refresh_token")
    
    def get_company_id(self) -> Optional[str]:
        """Get company ID."""
        return self._tokens.get("company_id")
    
    def clear_tokens(self) -> None:
        """Clear all stored tokens."""
        self._tokens = {}
        if self.token_file.exists():
            self.token_file.unlink()
        logger.info("Cleared all tokens")
    
    @property
    def is_authenticated(self) -> bool:
        """Check if we have valid authentication."""
        return self.get_access_token() is not None and self.get_company_id() is not None


class AutoQBOAuthenticator:
    """Handles QuickBooks Online OAuth authentication automatically."""
    
    def __init__(self, token_manager: Optional[QBOTokenManager] = None):
        """Initialize authenticator with optional token manager."""
        self.token_manager = token_manager or QBOTokenManager()
        self._auth_client = None
        self._server = None
        self._server_thread = None
        
    def _get_auth_client(self) -> AuthClient:
        """Get or create auth client."""
        if self._auth_client is None:
            self._auth_client = AuthClient(
                client_id=config.client_id,
                client_secret=config.client_secret,
                redirect_uri=config.redirect_uri,
                environment=config.environment,
                access_token=self.token_manager.get_access_token(),
                refresh_token=self.token_manager.get_refresh_token()
            )
        return self._auth_client
    
    def _start_callback_server(self) -> None:
        """Start HTTP server for OAuth callback."""
        try:
            self._server = HTTPServer(('localhost', 8080), CallbackHandler)
            self._server_thread = threading.Thread(target=self._server.serve_forever)
            self._server_thread.daemon = True
            self._server_thread.start()
            logger.info("Started callback server on localhost:8080")
        except Exception as e:
            logger.error(f"Error starting callback server: {e}")
            raise
    
    def _stop_callback_server(self) -> None:
        """Stop the callback server."""
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            if self._server_thread:
                self._server_thread.join(timeout=1)
            logger.info("Stopped callback server")
    
    def _perform_oauth_flow(self) -> bool:
        """Perform complete OAuth flow automatically."""
        try:
            if not config.is_configured:
                logger.error("QuickBooks configuration incomplete")
                return False
            
            # Start callback server
            self._start_callback_server()
            
            # Get authorization URL
            auth_client = self._get_auth_client()
            scopes = [Scopes.ACCOUNTING]
            auth_url = auth_client.get_authorization_url(scopes)
            
            logger.info("Opening browser for QuickBooks authorization...")
            print(f"\n🔐 QuickBooks Authentication Required")
            print(f"Opening browser to: {auth_url}")
            print(f"If browser doesn't open automatically, please visit the URL above.")
            
            # Open browser
            webbrowser.open(auth_url)
            
            # Wait for callback
            CallbackHandler.callback_url = None
            timeout = 300  # 5 minutes
            start_time = time.time()
            
            while CallbackHandler.callback_url is None:
                if time.time() - start_time > timeout:
                    logger.error("OAuth timeout - no callback received")
                    return False
                time.sleep(1)
            
            # Process callback
            callback_url = CallbackHandler.callback_url
            parsed_url = urlparse(callback_url)
            query_params = parse_qs(parsed_url.query)
            
            if 'error' in query_params:
                error = query_params['error'][0]
                logger.error(f"OAuth error: {error}")
                return False
            
            if 'code' not in query_params:
                logger.error("Authorization code not found in callback")
                return False
            
            auth_code = query_params['code'][0]
            company_id = query_params.get('realmId', [None])[0]
            
            if not company_id:
                logger.error("Company ID not found in callback")
                return False
            
            # Exchange code for tokens
            auth_client.get_bearer_token(auth_code)
            
            # Store tokens
            self.token_manager.store_tokens(
                access_token=auth_client.access_token,
                refresh_token=auth_client.refresh_token,
                company_id=company_id,
                expires_in=auth_client.x_refresh_token_expires_in or 3600
            )
            
            logger.info(f"✅ Successfully authenticated with QuickBooks (Company: {company_id})")
            return True
            
        except Exception as e:
            logger.error(f"Error in OAuth flow: {e}")
            return False
        finally:
            self._stop_callback_server()
    
    def _refresh_tokens(self) -> bool:
        """Refresh access tokens."""
        if not self.token_manager.get_refresh_token():
            logger.error("No refresh token available")
            return False
        
        try:
            auth_client = self._get_auth_client()
            auth_client.refresh()
            
            # Update stored tokens
            self.token_manager.store_tokens(
                access_token=auth_client.access_token,
                refresh_token=auth_client.refresh_token,
                company_id=self.token_manager.get_company_id(),
                expires_in=auth_client.x_refresh_token_expires_in or 3600
            )
            
            logger.info("✅ Successfully refreshed tokens")
            return True
            
        except Exception as e:
            logger.error(f"Error refreshing tokens: {e}")
            return False
    
    def ensure_authenticated(self) -> bool:
        """Ensure we have valid authentication, performing OAuth if needed."""
        # Check if already authenticated
        if self.token_manager.is_authenticated:
            logger.info("Already authenticated with QuickBooks")
            return True
        
        # Try to refresh tokens if we have a refresh token
        if self.token_manager.get_refresh_token():
            logger.info("Attempting to refresh tokens...")
            if self._refresh_tokens():
                return True
        
        # Perform full OAuth flow
        logger.info("Starting QuickBooks authentication...")
        return self._perform_oauth_flow()
    
    def get_authenticated_client(self) -> Optional[QuickBooks]:
        """Get authenticated QuickBooks client, handling auth automatically."""
        if not self.ensure_authenticated():
            logger.error("Failed to authenticate with QuickBooks")
            return None
        
        access_token = self.token_manager.get_access_token()
        company_id = self.token_manager.get_company_id()
        
        if not access_token or not company_id:
            logger.error("Missing access token or company ID after authentication")
            return None
        
        try:
            qb_client = QuickBooks(
                access_token=access_token,
                company_id=company_id,
                environment=config.environment
            )
            return qb_client
            
        except Exception as e:
            logger.error(f"Error creating QuickBooks client: {e}")
            return None
    
    @property
    def is_authenticated(self) -> bool:
        """Check if currently authenticated."""
        return self.token_manager.is_authenticated
    
    def get_company_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the authenticated company."""
        if not self.is_authenticated:
            return None
        
        return {
            "company_id": self.token_manager.get_company_id(),
            "environment": config.environment,
            "created_at": self.token_manager._tokens.get("created_at"),
            "expires_at": self.token_manager._tokens.get("expires_at")
        }


# Global authenticator instance
authenticator = AutoQBOAuthenticator()
