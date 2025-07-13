"""QuickBooks Online MCP Server with automatic authentication."""

import logging
from fastmcp import FastMCP

from .models import *
from .config import config
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(name)s:%(levelname)s: %(message)s'
)



# Initialize FastMCP server
mcp = FastMCP("qbo-mcp")

# Intentionally import after mcp definition to break circular dependency
from .tools import *  # ruff: noqa: E402
logger.debug("✅ Tools loaded")



