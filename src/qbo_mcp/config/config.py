"""Configuration settings for QBO MCP server."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent.parent / ".env"
if not load_dotenv(env_path):
    print(".env file not found in project root!")
else:
    print(f"🌐 .env file loaded from {env_path}")

if not os.getenv("QBO_CLIENT_ID") or not os.getenv("QBO_CLIENT_SECRET"):
    raise ValueError("QBO_CLIENT_ID and QBO_CLIENT_SECRET must be set in the environment variables!")

class QBOConfig():
    """Configuration class for QuickBooks Online integration."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.client_id: str = os.getenv("QBO_CLIENT_ID", "")
        self.client_secret: str = os.getenv("QBO_CLIENT_SECRET", "")
        self.redirect_uri: str = os.getenv("QBO_REDIRECT_URI", "http://localhost:8000/callback")
        self.scope: str = os.getenv("QBO_SCOPE", "com.intuit.quickbooks.accounting")
        self.environment: str = os.getenv("QBO_ENVIRONMENT", "sandbox")  # sandbox or production
        self.discovery_document_url: str = os.getenv(
            "QBO_DISCOVERY_DOCUMENT_URL",
            "https://developer.intuit.com/.well-known/openid_sandbox_configuration/"
        )
        
        # Token storage
        self.token_file: Path = Path(os.getenv("QBO_TOKEN_FILE", "qbo_tokens.json")).resolve()
        if not self.token_file.exists():
            self.token_file.touch()
            print(f"🪙 Created new token file at {self.token_file}")
            
        # Base URLs
        self.sandbox_base_url: str = "https://sandbox-quickbooks.api.intuit.com"
        self.production_base_url: str = "https://quickbooks.api.intuit.com"
        
    @property
    def base_url(self) -> str:
        """Get the appropriate base URL for the current environment."""
        return self.sandbox_base_url if self.environment != "production" else self.production_base_url
    
    @property
    def is_configured(self) -> bool:
        """Check if the minimum required configuration is present."""
        return bool(self.client_id and self.client_secret)
    
    def validate(self) -> list[str]:
        """Validate configuration and return list of missing/invalid settings."""
        errors = []
        
        if not self.client_id:
            errors.append("QBO_CLIENT_ID is required")
        if not self.client_secret:
            errors.append("QBO_CLIENT_SECRET is required")
        if self.environment not in ["sandbox", "production"]:
            errors.append("QBO_ENVIRONMENT must be 'sandbox' or 'production'")
            
        return errors


# Global configuration instance
config = QBOConfig()

__all__ = [
    "config",
    "QBOConfig",
]