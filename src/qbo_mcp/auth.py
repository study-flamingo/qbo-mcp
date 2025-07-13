"""Minimal authentication wrapper using intuit-oauth package."""

import json
import logging
from pathlib import Path
from typing import Any

from intuitlib.client import AuthClient
from intuitlib.exceptions import AuthClientError
from quickbooks import QuickBooks

from .config import config

logger = logging.getLogger()




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
            }
            
            self.token_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.token_file, 'w') as f:
                json.dump(tokens, f, indent=2)
            
            logger.info(f"Saved tokens to {self.token_file}")
            
        except Exception as e:
            logger.error(f"Error saving tokens: {e}")
    
    def ensure_authenticated(self) -> bool:
        """Ensure we have valid authentication by attempting to refresh tokens."""
        if not self.auth_client.refresh_token:
            logger.warning("No refresh token available. Authentication not possible.")
            return False

        try:
            self.auth_client.refresh()
            self._save_tokens()
            logger.info("✅ Refreshed tokens")
            return True
        except AuthClientError as e:
            logger.error(f"Refresh failed: {e.content} ({e.status_code}). Please obtain new tokens manually.")
            return False
    
    def get_authenticated_client(self) -> QuickBooks | None:
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
