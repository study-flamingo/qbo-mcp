"""
QuickBooks Online MCP Server - Entry Point
"""

import argparse
import logging
import sys

from .server import mcp
from .auth import authenticator
from .config import config



def main():

    # Configure logging
    logger = logging.getLogger()
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s:%(name)s:%(levelname)s: %(message)s",
    )

    # Setup argument parser
    parser = argparse.ArgumentParser(description="QuickBooks Online MCP Server")
    parser.add_argument(
        "-a", "--auth",
        action="store_true",
        help="Run the interactive OAuth2 authorization flow to get initial tokens.",
    )
    args = parser.parse_args()

    if args.auth:
        try:
            authenticator.ensure_authenticated()
        except Exception as e:
            logger.error(f"Failed to authenticate: {e}")
            sys.exit(1)
    else:
        # Check configuration on startup
        config_errors = config.validate()
        if config_errors:
            for error in config_errors:
                logger.error(f"❌ {error}")
        else:
            logger.info("✅ Config OK")
        
        # Run the server
        logger.info("💸 Starting QuickBooks Online MCP Server")
        mcp.run()

if __name__ == "__main__":
    main()