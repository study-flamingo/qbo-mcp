# src/qbo_mcp/services/qbo_client.py
"""
Handles the setup and lifecycle management of the QuickBooks Online SDK client.
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.exceptions import AuthorizationException

from ..config import QBOConfig
from ..models.common import QBOContext
from ..utils.auth import load_tokens, save_tokens # Import token utils

logger = logging.getLogger(__name__)


@asynccontextmanager
async def qbo_connection(config: QBOConfig) -> AsyncIterator[QBOContext]:
    """
    Establishes and manages a connection to QuickBooks Online.

    Handles fetching the refresh token, initializing the AuthClient and QuickBooks client,
    testing the connection, and saving refreshed tokens upon exit.

    Args:
        config: The QBOConfig object containing client ID, secret, etc.

    Yields:
        A QBOContext object containing the initialized QuickBooks client and AuthClient.

    Raises:
        ValueError: If the refresh token is missing or authentication fails.
        QuickbooksException: If there's an issue during connection testing.
    """
    logger.info("Initializing QBO connection...")
    # Initialize auth client
    auth_client = AuthClient(
        client_id=config.client_id,
        client_secret=config.client_secret,
        environment=config.environment,
        redirect_uri=config.redirect_uri
    )

    # Load refresh token from secure storage
    tokens = load_tokens() # Uses function from utils.auth
    refresh_token = tokens.get("refresh_token")

    if not refresh_token:
        # Provide a more informative error message
        logger.error("No refresh token found. Authentication required.")
        raise ValueError(
            "QuickBooks Online refresh token not found. "
            "Please run the authentication flow first using 'python main.py --auth'."
        )

    try:
        logger.debug("Initializing QuickBooks client...")
        client = QuickBooks(
            auth_client=auth_client,
            refresh_token=refresh_token,
            company_id=config.company_id, # Ensure company_id is loaded in config
            # minorversion=config.minor_version # Optional: specify minor version if needed
        )

        # Test the connection by fetching company info
        logger.debug("Testing QBO connection by fetching CompanyInfo...")
        client.get_company_info() # Use a method guaranteed to exist
        logger.info("QBO connection successful.")

    except AuthorizationException as e:
        logger.error(f"QBO Authorization failed: {e}", exc_info=True)
        raise ValueError(
            "QuickBooks Online authentication failed. "
            "The refresh token might be invalid or expired. "
            "Try running the auth flow again: 'python main.py --auth'"
        ) from e
    except Exception as e:
        logger.error(f"Failed to initialize QuickBooks client: {e}", exc_info=True)
        # Re-raise other exceptions (like network errors during connection test)
        raise

    qbo_ctx = QBOContext(client=client, auth_client=auth_client)
    try:
        yield qbo_ctx
    finally:
        logger.debug("Checking for refreshed QBO token...")
        # Save any refreshed tokens
        if client.refresh_token and client.refresh_token != refresh_token:
            logger.info("QBO refresh token has been updated. Saving new token.")
            save_tokens(client.refresh_token) # Uses function from utils.auth
        else:
            logger.debug("QBO refresh token unchanged.")
        logger.info("QBO connection context closed.")