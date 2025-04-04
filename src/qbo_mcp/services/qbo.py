import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from quickbooks import QuickBooks
from quickbooks.exceptions import AuthorizationException

from ..config import QBOConfig
from ..models import QBOContext


def get_token_path() -> Path:
    """Get the path to the token file."""
    return Path.home() / ".qbo-mcp" / "token.json"


def save_tokens(refresh_token: str) -> None:
    """Save tokens to a secure file."""
    token_path = get_token_path()
    token_path.parent.mkdir(parents=True, exist_ok=True)

    with open(token_path, "w") as f:
        json.dump({"refresh_token": refresh_token}, f)


def load_tokens() -> dict:
    """Load tokens from secure storage."""
    token_path = get_token_path()
    if not token_path.exists():
        return {}

    with open(token_path) as f:
        return json.load(f)


@asynccontextmanager
async def qbo_connection(config: QBOConfig) -> AsyncIterator[QBOContext]:
    """Create and manage QuickBooks Online connection."""
    # Initialize auth client with required scopes
    auth_client = AuthClient(
        client_id=config.client_id,
        client_secret=config.client_secret,
        environment=config.environment,
        redirect_uri=config.redirect_uri
    )

    # Try to load refresh token from secure storage
    tokens = load_tokens()
    refresh_token = tokens.get("refresh_token") or config.refresh_token

    if not refresh_token:
        raise ValueError(
            "No refresh token found. Please authenticate with QuickBooks Online first."
        )

    try:
        client = QuickBooks(
            auth_client=auth_client,
            refresh_token=refresh_token,
            company_id=config.company_id,
        )

        # Test the connection
        client.query("SELECT * FROM CompanyInfo LIMIT 1")

    except AuthorizationException:
        raise ValueError(
            "QuickBooks Online authentication failed. Please check your credentials."
        )

    try:
        yield QBOContext(client=client, auth_client=auth_client)
    finally:
        # Save any refreshed tokens
        if client.refresh_token != refresh_token:
            save_tokens(client.refresh_token)
