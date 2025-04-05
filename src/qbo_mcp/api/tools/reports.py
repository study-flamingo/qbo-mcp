# src/qbo_mcp/api/tools/reports.py
"""
MCP Tool definitions for generating QuickBooks Online reports and searching data.
"""
import logging

from mcp.server.fastmcp import Context

# Import the server instance (assuming it's defined in src/qbo_mcp/server.py)
from ...server import mcp
from ...models.common import QBOContext
from ...models.tools import TransactionFilter # Import specific input model
from ...services import reports as reports_service # Alias to avoid name clash
from ...utils.formatting import format_qbo_error

logger = logging.getLogger(__name__)

# Note: Assumes 'mcp' instance is accessible via import.

@mcp.tool()
async def get_profit_loss(ctx: Context, start_date: str, end_date: str) -> str:
    """Generate a Profit and Loss report for any date range. Dates should be in YYYY-MM-DD format."""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        # The service should ideally return structured data or handle formatting
        report_data = await reports_service.get_profit_loss(qbo_ctx, start_date, end_date)
        # For now, assume the service returns a string as before
        return report_data
    except Exception as e:
        return format_qbo_error(e)


@mcp.tool()
async def get_balance_sheet(ctx: Context, as_of_date: str) -> str:
    """Generate a Balance Sheet report as of any date. Date should be in YYYY-MM-DD format."""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        report_data = await reports_service.get_balance_sheet(qbo_ctx, as_of_date)
        return report_data
    except Exception as e:
        return format_qbo_error(e)


@mcp.tool()
async def get_aged_receivables(ctx: Context) -> str:
    """Get a report of all outstanding receivables grouped by age."""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        report_data = await reports_service.get_aged_receivables(qbo_ctx)
        return report_data
    except Exception as e:
        return format_qbo_error(e)


@mcp.tool()
async def search_transactions(
    ctx: Context,
    start_date: str | None = None,
    end_date: str | None = None,
    account_id: str | None = None,
) -> str:
    """Search for transactions with optional date range and account filters. Dates should be in YYYY-MM-DD format."""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        # Use the specific input model
        filter_criteria = TransactionFilter(
            start_date=start_date,
            end_date=end_date,
            account_id=account_id,
        )
        # Pass the filter object or its query representation to the service
        # The service layer should know how to handle the filter
        query = filter_criteria.to_query() # Assuming service expects the query string
        transactions = await reports_service.search_transactions(qbo_ctx, query)

        # Consider returning structured data instead of a simple string
        if not transactions:
            return "No transactions found matching the criteria."

        # Original formatting:
        return "\n".join(
            # Access attributes carefully, ensure they exist on the returned objects
            f"Transaction {getattr(txn, 'Id', 'N/A')}: {getattr(txn, 'TxnDate', 'N/A')} - {getattr(txn, 'Description', 'N/A')}"
            for txn in transactions
        )
    except Exception as e:
        return format_qbo_error(e)