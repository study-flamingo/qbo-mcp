import pytest
from qbo_mcp.server import mcp

@pytest.mark.asyncio
async def test_get_tools():
    """
    Test that the server exposes a non-empty set of MCP tools.
    """
    tools = await mcp.list_tools()
    assert isinstance(tools, list)
    assert len(tools) > 0 