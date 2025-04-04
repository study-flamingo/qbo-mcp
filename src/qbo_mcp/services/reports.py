from ..models import QBOContext


async def get_profit_loss(ctx: QBOContext, start_date: str, end_date: str) -> dict:
    """Generate Profit and Loss report for the specified date range."""
    # Assuming ctx.client has a method to call report endpoints
    # The actual method name might differ (e.g., make_request, call_api)
    # The return type is likely a dict representing the JSON response
    params = {"start_date": start_date, "end_date": end_date}
    # Use getattr to safely attempt calling the method, replace 'get_report' if needed
    report_func = getattr(ctx.client, "get_report", None)
    if report_func:
        return await report_func("ProfitAndLoss", params=params)
    else:
        # Fallback or error handling if the method doesn't exist
        raise NotImplementedError("Client does not have a 'get_report' method.")


async def get_balance_sheet(ctx: QBOContext, report_date: str) -> dict:
    """Generate Balance Sheet report as of specified date."""
    # Assuming ctx.client has a method to call report endpoints
    # QBO API parameter is typically 'report_date' or similar for Balance Sheet
    params = {"report_date": report_date}
    report_func = getattr(ctx.client, "get_report", None)
    if report_func:
        return await report_func("BalanceSheet", params=params)
    else:
        raise NotImplementedError("Client does not have a 'get_report' method.")


async def get_aged_receivables(ctx: QBOContext) -> dict:
    """Generate Aged Receivables report."""
    # Assuming ctx.client has a method to call report endpoints
    report_func = getattr(ctx.client, "get_report", None)
    if report_func:
        return await report_func("AgedReceivables", params={})
    else:
        raise NotImplementedError("Client does not have a 'get_report' method.")


async def search_transactions(ctx: QBOContext, query: str) -> list:
    """Search transactions using QBO query."""
    base_query = "SELECT * FROM Transaction"
    full_query = f"{base_query} WHERE {query}" if query else base_query
    return ctx.client.query(full_query)
