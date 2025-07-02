"""QuickBooks Online MCP Server with automatic authentication."""

import logging
from fastmcp import FastMCP

from .models import *
from .config import config


# Configure logging
logger = logging.getLogger("qbo_mcp")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(name)s:%(levelname)s: %(message)s'
)

# Initialize FastMCP server
mcp = FastMCP("qbo-mcp - QuickBooks Online MCP Server")
from .tools import *
logger.debug("✅ Tools loaded")



if __name__ == "__main__":
    # Check configuration on startup
    config_errors = config.validate()
    if config_errors:
        for error in config_errors:
            logger.error(f"{error}")
    else:
        logger.debug("✅ Config OK")
    
    # Run the server
    logger.info("💸 Starting QuickBooks Online MCP Server")
    mcp.run()
