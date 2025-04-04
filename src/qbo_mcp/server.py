import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from quickbooks.exceptions import QuickbooksException

from .config import load_config
from .models import QBOContext, TransactionFilter
from .services import qbo, reports, resources

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[QBOContext]:
    """Initialize and manage server lifecycle."""
    try:
        config = load_config()
        async with qbo.qbo_connection(config) as qbo_ctx:
            yield qbo_ctx
    except Exception as e:
        logger.error(f"Failed to initialize QBO connection: {e}")
        raise


# Create MCP server
mcp = FastMCP(
    "QuickBooks Online",
    lifespan=server_lifespan,
    description=(
        "Access QuickBooks Online financial data and reports. "
        "You can ask me to analyze financial statements, review cash flow, "
        "check on receivables, or search for specific transactions."
    ),
)


def format_qbo_error(e: Exception) -> str:
    """Format QuickBooks errors for Claude."""
    if isinstance(e, QuickbooksException):
        return f"QuickBooks error: {str(e)}"
    return f"An error occurred: {str(e)}"


# Resources
@mcp.resource("accounts://list")
def get_accounts(ctx: Context) -> str:
    """Get list of all accounts"""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        accounts = resources.get_accounts(qbo_ctx)
        return "\n".join(
            f"{acc.Id}: {acc.Name} ({acc.AccountType})" for acc in accounts
        )
    except Exception as e:
        logger.error(f"Failed to get accounts: {e}")
        return format_qbo_error(e)


@mcp.resource("customers://list")
def get_customers(ctx: Context) -> str:
    """Get list of all customers"""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        customers = resources.get_customers(qbo_ctx)
        return "\n".join(f"{cust.Id}: {cust.DisplayName}" for cust in customers)
    except Exception as e:
        logger.error(f"Failed to get customers: {e}")
        return format_qbo_error(e)


@mcp.resource("invoices://recent")
def get_recent_invoices(ctx: Context) -> str:
    """Get list of recent invoices"""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        invoices = resources.get_recent_invoices(qbo_ctx)
        return "\n".join(
            f"Invoice {inv.Id}: {inv.CustomerRef.name} - ${inv.TotalAmt}"
            for inv in invoices
        )
    except Exception as e:
        logger.error(f"Failed to get recent invoices: {e}")
        return format_qbo_error(e)


# Tools
@mcp.tool()
async def get_profit_loss(ctx: Context, start_date: str, end_date: str) -> str:
    """Generate a Profit and Loss report for any date range. Dates should be in YYYY-MM-DD format."""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        return await reports.get_profit_loss(qbo_ctx, start_date, end_date)
    except Exception as e:
        logger.error(f"Failed to generate P&L report: {e}")
        return format_qbo_error(e)


@mcp.tool()
async def get_balance_sheet(ctx: Context, as_of_date: str) -> str:
    """Generate a Balance Sheet report as of any date. Date should be in YYYY-MM-DD format."""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        return await reports.get_balance_sheet(qbo_ctx, as_of_date)
    except Exception as e:
        logger.error(f"Failed to generate balance sheet: {e}")
        return format_qbo_error(e)


@mcp.tool()
async def get_aged_receivables(ctx: Context) -> str:
    """Get a report of all outstanding receivables grouped by age."""
    try:
        qbo_ctx: QBOContext = ctx.request_context.lifespan_context
        return await reports.get_aged_receivables(qbo_ctx)
    except Exception as e:
        logger.error(f"Failed to generate aged receivables report: {e}")
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
        filter = TransactionFilter(
            start_date=start_date,
            end_date=end_date,
            account_id=account_id,
        )
        transactions = await reports.search_transactions(qbo_ctx, filter.to_query())
        return "\n".join(
            f"Transaction {txn.Id}: {txn.TxnDate} - {txn.Description}"
            for txn in transactions
        )
    except Exception as e:
        logger.error(f"Failed to search transactions: {e}")
        return format_qbo_error(e)


# Prompts
@mcp.prompt()
def analyze_cash_flow() -> str:
    """Guide for analyzing cash flow"""
    return """I'll help you analyze the company's cash flow situation. I'll:

1. Review the current balance sheet to assess cash position and working capital
2. Check aged receivables to understand collection status
3. Identify any concerning trends or potential cash flow issues
4. Provide specific recommendations for improving cash flow

Would you like me to proceed with this analysis?"""


@mcp.prompt()
def monthly_review() -> str:
    """Guide for monthly financial review"""
    today = datetime.now()
    first_of_month = today.replace(day=1)
    last_month_end = first_of_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    return f"""I'll help you review the financial results for last month. I'll:

1. Analyze the P&L statement from {last_month_start.strftime("%B %d")} to {last_month_end.strftime("%B %d")}
2. Review the balance sheet as of {last_month_end.strftime("%B %d")}
3. Highlight key metrics and significant changes
4. Identify areas that need attention
5. Suggest specific actions for improvement

Would you like me to proceed with this review?"""


@mcp.prompt()
def accounts_receivable_analysis() -> str:
    """Guide for AR analysis"""
    return """I'll help you analyze the accounts receivable situation. I'll:

1. Review the aged receivables report
2. Identify overdue accounts and aging patterns
3. Calculate key collection metrics
4. Recommend specific strategies for improving collections

Would you like me to proceed with this analysis?"""
