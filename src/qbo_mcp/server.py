import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
# Removed datetime, timedelta, Context, QuickbooksException, TransactionFilter imports as they are no longer used directly here

from mcp.server.fastmcp import FastMCP # Only need FastMCP

from .config import load_config
from .models.common import QBOContext # Import QBOContext from models.common
from .services.qbo_client import qbo_connection # Import connection manager from qbo_client

# Import the api modules to register the decorated functions
from . import api # This implicitly imports api.__init__
from .api import prompts # Import prompts module
from .api import tools # Import tools package (__init__.py imports specific tool modules)

# Configure logging
logger = logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[QBOContext]:
    """Initialize and manage server lifecycle."""
    try:
        config = load_config()
        # Use the imported qbo_connection from services.qbo_client
        async with qbo_connection(config) as qbo_ctx:
            yield qbo_ctx
    except Exception as e:
        logger.error(f"Failed to initialize QBO connection: {e}")
        raise


mcp = FastMCP(
    "QBO MCP Server",
    lifespan=server_lifespan,
    instructions="""Quickbooks MCP Server\n\n
        Access QuickBooks Online financial data and reports. You can ask
        me to analyze financial statements, review cash flow, check on
        receivables, or search for specific transactions.""" # TODO: add parameter descriptions
)


# Tool, Prompt, and formatting functions have been moved to the api and utils packages.
# Importing api.tools and api.prompts above ensures the decorators register them with the 'mcp' instance.
