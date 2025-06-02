from .server import mcp


def main():
    """Run the QBO MCP server."""
    mcp.run()


__all__ = ["mcp", "main"]
