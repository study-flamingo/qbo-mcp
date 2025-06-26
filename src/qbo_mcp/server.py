"""QuickBooks Online MCP Server with automatic authentication."""

import logging
from datetime import date, datetime
from typing import Any
from fastmcp import FastMCP
from pydantic import BaseModel, Field

from .models import *
from .auth import authenticator
from .config import config


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(name)s:%(levelname)s: %(message)s'
)
logger = logging.getLogger("qbo_mcp")

# Initialize FastMCP server
mcp = FastMCP("qbo-mcp - QuickBooks Online MCP Server")



if __name__ == "__main__":
    # Check configuration on startup
    config_errors = config.validate()
    if config_errors:
        print("⚠️  Configuration Issues:")
        for error in config_errors:
            print(f"   - {error}")
        print("\nPlease update your .env file with QuickBooks app credentials.")
        print("See README.md for setup instructions.")
    else:
        print("✅ Configuration validated")
    
    # Run the server
    print("🚀 Starting QuickBooks Online MCP Server...")
    mcp.run()
