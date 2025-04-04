"""
QuickBooks Online MCP Server - Entry Point

This file serves as the entry point for the QuickBooks Online MCP server.
It imports and runs the server implementation from the src/qbo_mcp package.
"""

import logging
import sys

# Add the src directory to the Python path if needed
# import sys
# from pathlib import Path
# sys.path.insert(0, str(Path(__file__).parent))

# Import the server from the package
from src.qbo_mcp.server import mcp

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    # Run the server
    try:
        mcp.run()
    except Exception as e:
        logging.error(f"Failed to start server: {e}")
        sys.exit(1)
