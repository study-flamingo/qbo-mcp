"""Minimal authentication wrapper using intuit-oauth package.

Design notes
------------
* Construction is **side-effect free**: no network calls and no browser are
  triggered until a token is actually needed. ``AuthClient`` performs a
  discovery request in its constructor, so it is built lazily.
* ``ensure_authenticated`` refreshes only when the stored access token is
  missing or near expiry, instead of refreshing on every tool call.
* The interactive OAuth flow is invoked lazily (first authenticated use), never
  at import time.
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Any

from intuitlib.client import AuthClient
from quickbooks import QuickBooks

from qbo_mcp.config import QBOConfig, config
from qbo_mcp.oauth_flow import run_interactive_oauth

logger = logging.getLogger(__name__)

# Refresh this many seconds before the access token actually expires.
_TOKEN_REFRESH_SKEW_SECONDS = 60


class QBOService:
    """
    Manages QuickBooks Online (QBO) authentication, token management, and client creation.

    This service wraps the intuit-oauth AuthClient and provides methods to ensure valid
    authentication, handle token persistence, and return authenticated QuickBooks client
    instances for API access.
    """

    def __init__(self, config: QBOConfig):
        """
        Initialize the QBOService with configuration and load any existing tokens.

        No network I/O or interactive prompt happens here; the AuthClient is created
        lazily on first use.

        Args:
            config (QBOConfig): Configuration object containing credentials and file paths.
        """
        self.config = config
        self.token_file = self.config.token_file
        self._auth_client: AuthClient | None = None
        self._tokens: dict[str, Any] = {}
        self._load_tokens()
        self.qbo: QuickBooks | None = None
        logger.info("QBOService initialized (lazy auth)!")

    # -- lazy AuthClient -------------------------------------------------------
    @property
    def auth_client(self) -> AuthClient:
        """Return the AuthClient, constructing it (and its discovery call) on demand."""
        if self._auth_client is None:
            ac = AuthClient(
                client_id=self.config.client_id,
                client_secret=self.config.client_secret,
                redirect_uri=self.config.redirect_uri,
                environment=self.config.environment,
            )
            ac.access_token = self._tokens.get("access_token")
            ac.refresh_token = self._tokens.get("refresh_token")
            ac.environment = self._tokens.get("environment", self.config.environment)
            ac.realm_id = self._tokens.get("realm_id")
            self._auth_client = ac
        return self._auth_client

    # -- token loading / persistence ------------------------------------------
    def _load_tokens(self) -> None:
        """
        Load tokens from disk or environment variables into memory.

        Does NOT start an interactive session if tokens are missing; the flow is
        deferred until ``ensure_authenticated`` is called.
        """
        tokens: dict[str, Any] = {}
        try:
            with open(self.token_file, "r") as f:
                tokens = json.load(f)
            logger.info(f"Loaded tokens from {self.token_file}")
        except FileNotFoundError:
            logger.warning(f"Token file not found at {self.token_file}")
        except Exception as e:
            logger.warning(f"Error reading token file: {str(e)}")

        if not tokens.get("access_token"):
            env_tokens = {
                "access_token": os.getenv("QBO_ACCESS_TOKEN"),
                "refresh_token": os.getenv("QBO_REFRESH_TOKEN"),
                "environment": os.getenv("QBO_ENVIRONMENT", self.config.environment),
                "realm_id": os.getenv("QBO_REALM_ID"),
            }
            env_tokens = {k: v for k, v in env_tokens.items() if v is not None}
            if env_tokens.get("access_token"):
                tokens = env_tokens
                logger.info("Loaded tokens from environment variables.")
            else:
                logger.warning("No tokens found in environment variables.")

        self._tokens = tokens
        if not tokens.get("access_token"):
            logger.info("No tokens available yet; interactive auth will run on first use if needed.")

    def _store_expiry(self) -> None:
        """Record the access-token expiry (epoch seconds) using the client's expires_in."""
        expires_in = getattr(self._auth_client, "expires_in", None)
        if expires_in:
            self._tokens["expires_at"] = time.time() + float(expires_in)

    def _save_tokens(self, tokens: dict | None = None) -> None:
        """Persist tokens to disk (0600) so the refresh token survives restarts."""
        try:
            if tokens is None:
                ac = self._auth_client
                tokens = dict(self._tokens)
                if ac is not None:
                    tokens.update(
                        {
                            "access_token": ac.access_token,
                            "refresh_token": ac.refresh_token,
                            "environment": ac.environment,
                            "realm_id": ac.realm_id,
                        }
                    )
            self._tokens = tokens
            self.token_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.token_file, "w") as f:
                json.dump(tokens, f, indent=2)
            try:
                os.chmod(self.token_file, 0o600)
            except OSError:
                pass
            logger.info(f"💾  Saved tokens to {self.token_file}")
        except Exception as e:
            logger.error(f"Error saving tokens: {str(e)}")

    # -- authentication --------------------------------------------------------
    def ensure_authenticated(self, interactive: bool = True) -> bool:
        """
        Ensure a valid access token is available.

        - If a non-expired access token is loaded, does nothing (no network call).
        - Otherwise refreshes using the refresh token.
        - If no tokens exist and ``interactive`` is True, runs the interactive OAuth flow.

        Returns:
            bool: True if authentication is ready.
        Raises:
            ValueError: if authentication cannot be completed.
        """
        ac = self.auth_client

        # Fast path: access token still valid.
        expires_at = self._tokens.get("expires_at")
        if ac.access_token and expires_at:
            try:
                if time.time() < float(expires_at) - _TOKEN_REFRESH_SKEW_SECONDS:
                    return True
            except (TypeError, ValueError):
                pass

        # Refresh with the refresh token.
        if ac.access_token and ac.refresh_token:
            try:
                ac.refresh()
                self._store_expiry()
                self._save_tokens()
                logger.info("Tokens refreshed successfully!")
                return True
            except Exception as e:
                logger.error(f"Token refresh error: {str(e)}")

        # No usable tokens: run interactive OAuth only if allowed.
        if interactive:
            logger.info("No valid tokens; starting interactive OAuth flow...")
            tokens = run_interactive_oauth(ac, self.config.scopes)
            ac.access_token = tokens.get("access_token")
            ac.refresh_token = tokens.get("refresh_token")
            ac.environment = tokens.get("environment", self.config.environment)
            ac.realm_id = tokens.get("realm_id")
            self._store_expiry()
            self._save_tokens()
            return True

        raise ValueError("No valid access or refresh token found and interactive auth is disabled!")

    def get_authenticated_client(self) -> QuickBooks:
        """
        Return an authenticated QuickBooks client, ensuring valid tokens.

        Returns:
            QuickBooks: An authenticated QuickBooks client instance.
        Raises:
            ValueError: If authentication fails or required tokens are missing.
        """
        if not self.ensure_authenticated():
            raise ValueError("Could not authenticate for QuickBooks client.")
        ac = self.auth_client
        if not (ac.access_token and ac.refresh_token and ac.realm_id):
            raise ValueError("Missing required tokens or realm_id for QuickBooks client.")
        try:
            self.qbo = QuickBooks(
                auth_client=ac,
                refresh_token=ac.refresh_token,
                realm_id=ac.realm_id,
            )
        except Exception as e:
            logger.error(f"QBO Service error: {str(e)}")
            raise ValueError(f"QBO Service error: {str(e)}")
        return self.qbo

    def revoke_tokens(self) -> bool:
        """
        Revoke the current refresh token and clear persisted/in-memory tokens.

        Returns:
            bool: True if tokens were revoked, False if no refresh token was present.
        Raises:
            ValueError: If revocation fails.
        """
        try:
            ac = self.auth_client
            if ac.refresh_token:
                ac.revoke()
                if self.token_file.exists():
                    self.token_file.unlink()
                ac.access_token = None
                ac.refresh_token = None
                ac.realm_id = None
                ac.environment = "sandbox"
                self._tokens = {}
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
        ac = self.auth_client
        if not (ac.access_token and ac.refresh_token and ac.realm_id):
            return {"error": "Not authenticated"}
        return {
            "realm_id (company_id)": ac.realm_id,
            "environment": self.config.environment,
            "has_access_token": bool(ac.access_token),
            "has_refresh_token": bool(ac.refresh_token),
        }


# Global authenticator instance (constructed lazily; no I/O at import).
qbo_service = QBOService(config=config)

__all__ = ["qbo_service"]
