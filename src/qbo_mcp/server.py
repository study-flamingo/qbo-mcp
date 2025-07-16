"""QuickBooks Online MCP Server with automatic authentication."""

import logging
from fastmcp import FastMCP

from .models import *
from .config import *
from .auth import *
from dotenv import load_dotenv
from .tools import *


# Configure logging
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(name)s:%(levelname)s: %(message)s'
)

mcp = FastMCP("qbo-mcp")

register_tools(mcp)
