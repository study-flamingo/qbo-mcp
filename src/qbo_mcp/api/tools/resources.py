# src/qbo_mcp/api/tools/resources.py
"""
MCP Tool definitions for accessing QuickBooks Online resources like accounts, customers, etc.
"""
import logging

from mcp.server.fastmcp import Context

# Import the server instance (assuming it's defined in src/qbo_mcp/server.py)
# We need this to use the @mcp.tool decorator
from ...server import mcp
from ...models.common import QBOContext
from ...services import resources as resources_service # Alias to avoid name clash
from ...utils.formatting import format_qbo_error

logger = logging.getLogger(__name__)

# Note: The 'mcp' instance needs to be accessible here.
# This might require adjusting how 'mcp' is defined or imported in server.py
# if it causes circular dependencies later. For now, assume direct import works.

@mcp.tool()
def get_accounts(ctx: Context) -> str:
    """Get list of all accounts"""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        accounts = resources_service.get_accounts(qbo_ctx)
        # Consider returning structured data (list of dicts/models) instead of pre-formatted string
        # For now, keeping the original formatting:
        return "\n".join(
            f"{acc.Id}: {acc.Name} ({acc.AccountType})" for acc in accounts
        )
    except Exception as e:
        # Use the centralized error formatter
        return format_qbo_error(e)


@mcp.tool()
def get_customers(ctx: Context) -> str:
    """Get list of all customers"""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        customers = resources_service.get_customers(qbo_ctx)
        return "\n".join(f"{cust.Id}: {cust.DisplayName}" for cust in customers)
    except Exception as e:
        return format_qbo_error(e)


@mcp.tool()
def get_recent_invoices(ctx: Context) -> str:
    """Get list of recent invoices"""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        invoices = resources_service.get_recent_invoices(qbo_ctx)
        # Consider adding date or status to the output
        return "\n".join(
            f"Invoice {inv.Id}: {inv.CustomerRef.name} - ${inv.TotalAmt}"
            for inv in invoices
        )
    except Exception as e:
        return format_qbo_error(e)