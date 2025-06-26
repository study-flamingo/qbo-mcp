"""
QuickBooks Online MCP Server - Entry Point

This file serves as the entry point for the QuickBooks Online MCP server.
It imports and runs the server implementation from the src/qbo_mcp package.
"""

import argparse
import logging
import sys

from .server import mcp
from .auth import authenticator

logger = logging.getLogger("qbo_mcp")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(name)s:%(levelname)s: %(message)s",
)

def main():

    # Setup argument parser
    parser = argparse.ArgumentParser(description="QuickBooks Online MCP Server")
    parser.add_argument(
        "-a", "--auth",
        action="store_true",
        nargs=2,
        help="Run the interactive OAuth2 authorization flow to get initial tokens.",
    )
    args = parser.parse_args()

    if args.auth:
        auth_path = args.auth[0]
        authenticator.ensure_authenticated(path=auth_path)
    else:
        # Run the MCP server
        logging.info("Starting MCP server...")
        try:
            mcp.run()
        except Exception as e:
            logging.error(f"Failed to start server: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()