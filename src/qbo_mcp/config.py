import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv


@dataclass
class QBOConfig:
    """QuickBooks Online configuration settings."""

    client_id: str
    client_secret: str
    environment: Literal["sandbox", "production"]
    redirect_uri: str
    company_id: str | None = None # Keep for now, might be removable if QuickBooks client gets it automatically


def load_config() -> QBOConfig:
    """Load QBO configuration from environment variables, optionally loading from ~/.qbo-mcp/.env"""
    env_path = Path.home() / ".qbo-mcp"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)

    return QBOConfig(
        client_id=os.getenv("QBO_CLIENT_ID", ""),
        client_secret=os.getenv("QBO_CLIENT_SECRET", ""),
        environment=os.getenv("QBO_ENVIRONMENT", "sandbox"),
        redirect_uri=os.getenv("QBO_REDIRECT_URI", "http://localhost:8000/callback"),
        company_id=os.getenv("QBO_COMPANY_ID"),
        # refresh_token is no longer loaded here, managed by qbo.py's token.json
    )
