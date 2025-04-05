# src/qbo_mcp/utils/auth.py
"""
Handles QuickBooks Online OAuth2 authentication flow and token management.
"""

import json
import logging
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError

from ..config import load_config # Import config loader

logger = logging.getLogger(__name__)


def get_token_path() -> Path:
    """Get the path to the token file."""
    # Store token in user's home directory for persistence across runs
    return Path.home() / ".qbo-mcp" / "token.json"


def save_tokens(refresh_token: str) -> None:
    """Save the refresh token to a secure file."""
    token_path = get_token_path()
    try:
        token_path.parent.mkdir(parents=True, exist_ok=True)
        # Set restrictive permissions (example for Unix-like systems)
        # On Windows, file permissions are handled differently.
        # Consider using platform-specific methods if stricter security is needed.
        # token_path.parent.chmod(0o700) # Ensure directory is private
        with open(token_path, "w") as f:
            json.dump({"refresh_token": refresh_token}, f)
        # token_path.chmod(0o600) # Ensure file is private
        logger.info(f"Refresh token saved successfully to {token_path}")
    except OSError as e:
        logger.error(f"Error saving token file at {token_path}: {e}")
        # Decide if this should be a fatal error or just a warning
        raise  # Re-raise for now


def load_tokens() -> dict:
    """Load tokens from secure storage."""
    token_path = get_token_path()
    if not token_path.exists():
        logger.warning(f"Token file not found at {token_path}. Run auth flow.")
        return {}
    try:
        # Check permissions before reading (example for Unix-like)
        # stat_result = token_path.stat()
        # if stat_result.st_mode & 0o077: # Check if others/group have permissions
        #     logger.warning(f"Token file {token_path} has insecure permissions. Please restrict access.")
        #     # Optionally, refuse to load or attempt to fix permissions

        with open(token_path) as f:
            tokens = json.load(f)
            if "refresh_token" not in tokens:
                logger.error(f"Token file {token_path} is missing 'refresh_token'.")
                return {}
            return tokens
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from token file: {token_path}")
        return {}
    except OSError as e:
        logger.error(f"Error reading token file at {token_path}: {e}")
        return {}


def run_auth_flow():
    """Guides the user through the OAuth2 authorization process."""
    # This function is intended to be run interactively from the command line.
    logger.info("Starting QuickBooks Online OAuth2 authorization flow...")
    try:
        config = load_config()
        if not config.client_id or not config.client_secret:
            logger.error(
                "Missing QBO_CLIENT_ID or QBO_CLIENT_SECRET environment variables."
            )
            logger.error(
                "Please set these in your environment or in ~/.qbo-mcp/.env"
            )
            sys.exit(1)

        auth_client = AuthClient(
            client_id=config.client_id,
            client_secret=config.client_secret,
            redirect_uri=config.redirect_uri,
            environment=config.environment,
        )

        # Define scopes required by your application
        scopes = [Scopes.ACCOUNTING] # Add other scopes like Scopes.PAYMENT if needed

        url = auth_client.get_authorization_url(scopes)

        print("-" * 80)
        print("Please visit the following URL in your browser to authorize this application:")
        print(f"\n{url}\n")
        print("After authorization, you will be redirected to your configured redirect URI.")
        print("Copy the FULL redirected URL from your browser's address bar and paste it below.")
        print("-" * 80)

        callback_url = input("Paste the full callback URL here: ").strip()

        # Parse the callback URL
        parsed_url = urlparse(callback_url)
        query_params = parse_qs(parsed_url.query)

        auth_code = query_params.get("code", [None])[0]
        realm_id = query_params.get("realmId", [None])[0]
        # state = query_params.get("state", [None])[0] # Optional: verify state if you passed one

        if not auth_code or not realm_id:
            logger.error("Could not extract authorization code or realm ID from the callback URL.")
            logger.error(f"Extracted params: code={auth_code}, realmId={realm_id}")
            sys.exit(1)

        logger.info("Exchanging authorization code for tokens...")
        auth_client.get_bearer_token(auth_code, realm_id=realm_id)

        # Save the refresh token securely using the function in this module
        save_tokens(auth_client.refresh_token)
        # get_token_path() is also available in this module

        print("\n" + "=" * 80)
        print("Authorization Successful!")
        print(f"Refresh token has been saved securely to {get_token_path()}")
        print("Please add the following line to your environment variables or ~/.qbo-mcp/.env file:")
        print(f"QBO_COMPANY_ID={auth_client.realm_id}")
        print("=" * 80 + "\n")
        logger.info("Authorization flow completed successfully. Refresh token saved, Company ID displayed.")
        sys.exit(0) # Exit after successful auth flow

    except AuthClientError as e:
        logger.error(f"OAuth Error Status Code: {e.status_code}")
        logger.error(f"OAuth Error Response: {e.content}")
        logger.error(f"Intuit Transaction ID: {e.intuit_tid}")
        logger.error("Authorization failed. Please check your credentials and redirect URI.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred during authorization: {e}", exc_info=True)
        sys.exit(1)