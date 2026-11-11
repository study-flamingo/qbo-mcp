"""
QuickBooks Online MCP Server - Entry Point
"""

import argparse
import logging
import os
import sys

from .server import mcp
from .auth import qbo_service
from .config import config



def main():

    # Configure logging (DEBUG only when QBO_DEBUG is set)
    logging.basicConfig(
        level=logging.DEBUG if os.getenv("QBO_DEBUG") else logging.INFO,
        format="%(asctime)s:%(name)s:%(levelname)s: %(message)s",
    )
    logger = logging.getLogger(__name__)

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
            qbo_service.ensure_authenticated()
        except Exception as e:
            logger.error(f"Failed to authenticate: {str(e)}")
            sys.exit(1)
    else:
        # Check configuration on startup
        config_errors = config.validate()
        if config_errors:
            for error in config_errors:
                logger.error(f"❌ {error}")
            raise ValueError("Could not start: {config_errors. }")
        else:
            logger.info("✅ Config OK")
        
            # Run the server
            logger.info("💸 Starting QuickBooks Online MCP Server")
            mcp.run()

if __name__ == "__main__":
    main()