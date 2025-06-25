"""
QuickBooks Online MCP Server - Entry Point

This file serves as the entry point for the QuickBooks Online MCP server.
It imports and runs the server implementation from the src/qbo_mcp package.
"""

import argparse
import logging
import sys
# Removed unused imports: parse_qs, urlparse, AuthClient, Scopes, AuthClientError

# Add the src directory to the Python path if needed
# from pathlib import Path
# sys.path.insert(0, str(Path(__file__).parent))
# Import the server and the new auth utility function
from src.qbo_mcp.server import mcp
from src.qbo_mcp.utils.auth import run_auth_flow
# Removed unused imports: load_config, get_token_path, save_tokens


# run_auth_flow function has been moved to src.qbo_mcp.utils.auth

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Setup argument parser
    parser = argparse.ArgumentParser(description="QuickBooks Online MCP Server")
    parser.add_argument(
        "--auth",
        action="store_true",
        help="Run the interactive OAuth2 authorization flow to get initial tokens.",
    )
    args = parser.parse_args()

    if args.auth:
        run_auth_flow()
    else:
        # Run the MCP server
        logging.info("Starting MCP server...")
        try:
            mcp.run()
        except Exception as e:
            logging.error(f"Failed to start server: {e}")
            sys.exit(1)
