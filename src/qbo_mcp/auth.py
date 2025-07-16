"""Minimal authentication wrapper using intuit-oauth package."""

import json
import logging
import os
from pathlib import Path
from typing import Any

from intuitlib.client import AuthClient
from quickbooks import QuickBooks

from .config import QBOConfig, config

logger = logging.getLogger()



class QBOService:
    """Manages QBO authentication, client creation, and QuickBooks Online API interactions."""
    
    def __init__(self, config: QBOConfig):
        """Initialize auth manager."""
        self.token_file = config.token_file
        
        try:
            try:
                with open(self.token_file, 'r') as f:
                    tokens = json.load(f)
            except FileNotFoundError:
                logger.warning(f"No token file found at {self.token_file}")
                tokens = {}
        except Exception as e:
            raise ValueError(f"Error reading token file: {str(e)}")
            
        self.access_token: str | None = tokens.get("access_token")
        self.refresh_token: str | None = tokens.get("refresh_token")
        
        try:
            self.auth_client = AuthClient(
                client_id=config.client_id,
                client_secret=config.client_secret,
                redirect_uri=config.redirect_uri,
                environment=config.environment,
                access_token=self.access_token,
                refresh_token=self.refresh_token,
            )
        except Exception as e:
            raise ValueError(f"QBOService auth client initialization error: {str(e)}")
        
        try:
            self.qbo = QuickBooks(
                auth_client=self.auth_client,
                refresh_token=self.auth_client.refresh_token,
                company_id=self.auth_client.realm_id,
            )
        except Exception as e:
            raise ValueError(f"QBOService startup error: {str(e)}")
        
        logger.info("QBOService initialized!")
    
    def _load_tokens(self) -> None:
        """Load tokens from disk into AuthClient."""
        try:
            with open(self.token_file, 'r') as f:
                tokens = json.load(f)
            if not tokens:
                raise ValueError(f"No tokens found in {self.token_file}!")
            logger.info(f"Loaded tokens from {self.token_file}")
        except FileNotFoundError:
            logger.warning(f"Token file not found at {self.token_file}")
            # If no token file, look for tokens in environment variables
            tokens = {
                "access_token": os.getenv("QBO_ACCESS_TOKEN"),
                "refresh_token": os.getenv("QBO_REFRESH_TOKEN"),
                "realm_id": os.getenv("QBO_REALM_ID", "sandbox")
            }
        if not all(tokens.values()):
            raise ValueError("Missing tokens in environment variables")

        # Set tokens directly on AuthClient - let it handle the rest
        self.auth_client.access_token = tokens.get('access_token')
        self.auth_client.refresh_token = tokens.get('refresh_token')
        self.auth_client.realm_id = tokens.get('realm_id')
            
            
    
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
            logger.error(f"Error saving tokens: {str(e)}")
    
    def ensure_authenticated(self) -> bool:
        """Ensure we have valid authentication by attempting to refresh tokens."""
        if not self.auth_client:
            raise ValueError("Auth client not found!")
        
        if not self.auth_client.refresh_token:
            raise ValueError("No refresh token available. Please obtain new tokens manually.")

        try:
            self.auth_client.refresh()
            self._save_tokens()
            logger.info("Tokens refreshed")
            return True
        except Exception as e:
            raise ValueError(f"Token refresh error: {str(e)}")
    
    def get_authenticated_client(self) -> QuickBooks:
        """Get authenticated QuickBooks client."""
        try:
            self.ensure_authenticated()
        except Exception as e:
            raise ValueError(f"Get client error: {str(e)}")
        
        if not self.auth_client:
            raise ValueError("Auth client not found!")
        
        if not self.auth_client.access_token or not self.auth_client.refresh_token:
            raise ValueError("Missing tokens after authentication")
        elif not self.auth_client.realm_id:
            raise ValueError("Missing realm ID after authentication")

        try:
            return QuickBooks(
                access_token=self.auth_client.access_token,
                company_id=self.auth_client.realm_id,
                environment=config.environment
            )
        except Exception as e:
            raise ValueError(f"Client creation error: {str(e)}")
    
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
        except Exception as e:
            raise ValueError(f"Revocation error: {str(e)}")
    
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
qbo_service = QBOService(config=config)

__all__ = ["qbo_service"]