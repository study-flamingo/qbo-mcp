import pytest
from qbo_mcp.server import mcp

@pytest.mark.asyncio
async def test_get_tools():
    """
    Test that the get_tools function returns a list of tools.
    """
    tools = await mcp.get_tools()
    assert isinstance(tools, dict)
    assert len(tools) > 0 