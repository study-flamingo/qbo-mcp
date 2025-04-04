"""
QuickBooks Online MCP Server - Package Entry Point

This file allows the qbo_mcp package to be executed directly
using `python -m qbo_mcp`. It imports and runs the server.
"""

import logging
import sys

# Assuming the server instance is defined in .server
# Adjust the import path if your server instance is located elsewhere within the package
try:
    from .server import mcp
except ImportError:
    # Handle cases where the script might be run in a way that relative imports fail
    # This might happen during development or testing scenarios.
    # A more robust solution might involve adjusting sys.path or using absolute imports
    # if the package structure guarantees it.
    logging.error("Failed to import server using relative import. Ensure the package structure is correct or adjust imports.")
    # Attempt absolute import as a fallback, assuming 'src' is in PYTHONPATH or similar
    try:
        from src.qbo_mcp.server import mcp
        logging.info("Successfully imported server using absolute path fallback.")
    except ImportError:
         logging.critical("Failed to import server using both relative and absolute paths. Cannot start server.")
         sys.exit(1)


def main():
    """Configures logging and runs the MCP server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logging.info("Starting server via package entry point (__main__.py)...")
    try:
        mcp.run()
    except Exception as e:
        logging.error(f"Failed to start server: {e}")
        sys.exit(1)

# This check ensures the main function runs only when the package is executed directly
if __name__ == "__main__":
    main()