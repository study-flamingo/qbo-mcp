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
from qbo_mcp.oauth_flow import run_interactive_oauth

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
        self.config = config
        self.token_file = self.config.token_file
        self.auth_client = AuthClient(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            redirect_uri=self.config.redirect_uri,
            environment=self.config.environment,
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
                "environment": os.getenv("QBO_ENVIRONMENT", "sandbox"),
                "realm_id": os.getenv("QBO_REALM_ID"),
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
            tokens = run_interactive_oauth(self.auth_client, self.config.scopes)
            self._save_tokens(tokens)
            logger.info("Successfully obtained and saved tokens from initial OAuth flow.")

        # Set tokens on auth_client
        self.auth_client.access_token = tokens.get('access_token')
        self.auth_client.refresh_token = tokens.get('refresh_token')
        self.auth_client.environment = tokens.get('environment', 'sandbox')
        self.auth_client.realm_id = tokens.get('realm_id')

    def _save_tokens(self, tokens=None) -> None:
        """
        Persist the current AuthClient tokens to disk.

        Saves the access token, refresh token, environment, and realm_id to the configured token file.
        """
        try:
            if tokens is None:
                tokens = {
                    'access_token': self.auth_client.access_token,
                    'refresh_token': self.auth_client.refresh_token,
                    'environment': self.auth_client.environment,
                    'realm_id': self.auth_client.realm_id,
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
        if not self.auth_client.access_token or not self.auth_client.refresh_token:
            raise ValueError("No valid access or refresh token found!")
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
        configured with the current AuthClient and realm_id.

        Returns:
            QuickBooks: An authenticated QuickBooks client instance.
        Raises:
            ValueError: If authentication fails or required tokens are missing.
        """
        if not (self.auth_client.access_token and self.auth_client.refresh_token and self.auth_client.realm_id):
            raise ValueError("Missing required tokens or realm_id for QuickBooks client.")
        if not self.ensure_authenticated():
            raise ValueError("Could not refresh tokens for QuickBooks client.")
        try:
            self.qbo = QuickBooks(
                auth_client=self.auth_client,
                refresh_token=self.auth_client.refresh_token,
                realm_id=self.auth_client.realm_id,
            )
        except Exception as e:
            logger.error(f"QBO Service error: {str(e)}")
            raise ValueError(f"QBO Service error: {str(e)}")
        return self.qbo

    def revoke_tokens(self) -> bool:
        """
        Revoke the current refresh token and clear persisted tokens and in-memory tokens.

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
                # Clear in-memory tokens
                self.auth_client.access_token = None
                self.auth_client.refresh_token = None
                self.auth_client.realm_id = None
                self.auth_client.environment = 'sandbox'
                logger.info("✅ Revoked tokens and cleared in-memory state")
                return True
            return False
        except Exception as e:
            logger.error(f"Revocation error: {str(e)}")
            raise ValueError(f"Revocation error: {str(e)}")

    def get_company_info(self) -> dict[str, Any] | None:
        """
        Get basic company/environment info for the current authentication context.

        Returns:
            dict[str, Any] | None: Dictionary with company/environment info, or error if not authenticated.
        """
        if not (self.auth_client.access_token and self.auth_client.refresh_token and self.auth_client.realm_id):
            return {"error": "Not authenticated"}
        company_info = {
            "realm_id (company_id)": self.auth_client.realm_id,
            "environment": self.config.environment,
            "has_access_token": bool(self.auth_client.access_token),
            "has_refresh_token": bool(self.auth_client.refresh_token)
        }
        return company_info


# Global authenticator instance
qbo_service = QBOService(config=config)

__all__ = ["qbo_service"]