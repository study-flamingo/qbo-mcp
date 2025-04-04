"""QuickBooks Online MCP Server.

This package provides an MCP server that integrates with QuickBooks Online
to provide financial data and reporting capabilities.
"""

from .server import mcp


def main():
    """Run the QBO MCP server."""
    mcp.run()


__all__ = ["mcp", "main"]
