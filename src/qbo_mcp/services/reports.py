from quickbooks.objects.report import Report

from ..models import QBOContext


async def get_profit_loss(ctx: QBOContext, start_date: str, end_date: str) -> str:
    """Generate Profit and Loss report for the specified date range."""
    report = Report.profit_and_loss(
        qbo=ctx.client,
        start_date=start_date,
        end_date=end_date,
    )
    return report.get_report()


async def get_balance_sheet(ctx: QBOContext, as_of_date: str) -> str:
    """Generate Balance Sheet report as of specified date."""
    report = Report.balance_sheet(
        qbo=ctx.client,
        as_of=as_of_date,
    )
    return report.get_report()


async def get_aged_receivables(ctx: QBOContext) -> str:
    """Generate Aged Receivables report."""
    report = Report.aged_receivables(qbo=ctx.client)
    return report.get_report()


async def search_transactions(ctx: QBOContext, query: str) -> list:
    """Search transactions using QBO query."""
    base_query = "SELECT * FROM Transaction"
    full_query = f"{base_query} WHERE {query}" if query else base_query
    return ctx.client.query(full_query)
