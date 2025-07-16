import logging
from datetime import date, datetime, timedelta
from typing import Any, Optional
from typing_extensions import Annotated
import jsonschema
from fastmcp.server import FastMCP
from pydantic import Field

from .auth import authenticator
from .config import config
from .reports import (
    reports_generator,
    ReportPeriod,
    get_current_month_period,
    get_current_quarter_period,
    get_current_year_period,
    get_last_month_period
)
from .schemas import (
    PROFIT_LOSS_REQUEST_SCHEMA,
    BALANCE_SHEET_REQUEST_SCHEMA,
    CASH_FLOW_REQUEST_SCHEMA,
    AGING_REQUEST_SCHEMA,
    SALES_CUSTOMER_REQUEST_SCHEMA,
    EXPENSES_VENDOR_REQUEST_SCHEMA
)

logger = logging.getLogger()

# --- Helper functions migrated from models.py ---
def get_current_datetime(include: str | list[str] | None = None,
                         first_day_of_month: bool = False,
                         last_day_of_month: bool = False) -> str:
    """Helper function to get the current date and time.
    Args:
        include (str | list[str] | None): Optionally, a List of components to
            include in the format, or a single component as a string. If a list,
            each component can be one of the following:
            - "year", "month", "day", "hour", "minute", "second".
            If omitted (None), defaults to full datetime.
        first_day_of_month (bool): If True, sets the day to the first of the month.
        last_day_of_month (bool): If True, sets the day to the last of the month.
            (Overrides first_day_of_month if both are True)
    Returns:
        str: Current date and time formatted as a string. ("YYYY-MM-DD HH:MM:SS")
    """
    current_dt = datetime.now()
    if last_day_of_month:
        next_month = current_dt.replace(day=28) + timedelta(days=4)
        current_dt = next_month - timedelta(days=next_month.day)
    elif first_day_of_month:
        current_dt = current_dt.replace(day=1)
    format_str = ""
    if isinstance(include, str):
        include = [include]
    if include:
        if "year" in include:
            format_str += "%Y-"
        if "month" in include:
            format_str += "%m-"
        if "day" in include:
            format_str += "%d "
        if "hour" in include:
            format_str += "%H:"
        if "minute" in include:
            format_str += "%M:"
        if "second" in include:
            format_str += "%S"
    else:
        format_str = "%Y-%m-%d %H:%M:%S"
    return current_dt.strftime(format_str).strip()

# JSON Schema validation helper
def validate_json_schema(instance: dict, schema: dict, name: str = ""):
    try:
        jsonschema.validate(instance=instance, schema=schema)
    except jsonschema.ValidationError as e:
        raise ValueError(f"{name} JSON Schema validation error: {e.message}")


def parse_date(date_str: str) -> date:
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


# Refactored create_report_period to work with plain strings
def create_report_period(start_date: str | None, end_date: str | None) -> ReportPeriod:
    """Get ReportPeriod from string dates or default to current month."""
    if start_date and end_date:
        return ReportPeriod(
            start_date=parse_date(start_date),
            end_date=parse_date(end_date)
        )
    return get_current_month_period()


def _ensure_authenticated_and_handle_errors():
    """
    Helper function to ensure authentication and handle configuration/authentication errors.
    Raises ValueError if authentication fails or configuration is invalid.
    """
    config_errors = config.validate()
    if config_errors:
        raise ValueError(f"Configuration errors: {', '.join(config_errors)}. Please set up your .env file with QuickBooks app credentials.")
    
    if not authenticator.ensure_authenticated():
        raise ValueError("Failed to authenticate with QuickBooks Online. Please check your credentials and try again.")


def _generate_profit_loss_report(start_date: str | None, end_date: str | None, summarize_by: str = "Month") -> dict[str, Any]:
    _ensure_authenticated_and_handle_errors()
    input_dict = {
        "period": {"start_date": start_date, "end_date": end_date},
        "summarize_by": summarize_by
    }
    validate_json_schema(input_dict, PROFIT_LOSS_REQUEST_SCHEMA, name="ProfitLossRequest")
    period = create_report_period(start_date, end_date)
    report = reports_generator.get_profit_and_loss(period, summarize_by)
    return {
        "status": "success",
        "report_type": "Profit & Loss",
        "period": {
            "start_date": period.start_date.isoformat(),
            "end_date": period.end_date.isoformat()
        },
        "company_info": authenticator.get_company_info(),
        "data": report
    }

def _generate_balance_sheet_report(as_of_date: str | None, summarize_by: str = "Month") -> dict[str, Any]:
    _ensure_authenticated_and_handle_errors()
    input_dict = {
        "as_of_date": as_of_date,
        "summarize_by": summarize_by
    }
    validate_json_schema(input_dict, BALANCE_SHEET_REQUEST_SCHEMA, name="BalanceSheetRequest")
    as_of_date_dt = parse_date(as_of_date) if as_of_date else date.today()
    report = reports_generator.get_balance_sheet(as_of_date_dt, summarize_by)
    return {
        "status": "success",
        "report_type": "Balance Sheet",
        "as_of_date": as_of_date_dt.isoformat(),
        "company_info": authenticator.get_company_info(),
        "data": report
    }

def _generate_cash_flow_report(start_date: str | None, end_date: str | None) -> dict[str, Any]:
    _ensure_authenticated_and_handle_errors()
    input_dict = {
        "period": {"start_date": start_date, "end_date": end_date}
    }
    validate_json_schema(input_dict, CASH_FLOW_REQUEST_SCHEMA, name="CashFlowRequest")
    period = create_report_period(start_date, end_date)
    report = reports_generator.get_cash_flow(period)
    return {
        "status": "success",
        "report_type": "Cash Flow",
        "period": {
            "start_date": period.start_date.isoformat(),
            "end_date": period.end_date.isoformat()
        },
        "company_info": authenticator.get_company_info(),
        "data": report
    }

def _generate_ar_aging_report(as_of_date: str | None) -> dict[str, Any]:
    _ensure_authenticated_and_handle_errors()
    input_dict = {"as_of_date": as_of_date}
    validate_json_schema(input_dict, AGING_REQUEST_SCHEMA, name="AgingRequest")
    as_of_date_dt = parse_date(as_of_date) if as_of_date else date.today()
    report = reports_generator.get_accounts_receivable_aging(as_of_date_dt)
    return {
        "status": "success",
        "report_type": "Accounts Receivable Aging",
        "as_of_date": as_of_date_dt.isoformat(),
        "company_info": authenticator.get_company_info(),
        "data": report
    }

def _generate_ap_aging_report(as_of_date: str | None) -> dict[str, Any]:
    _ensure_authenticated_and_handle_errors()
    input_dict = {"as_of_date": as_of_date}
    validate_json_schema(input_dict, AGING_REQUEST_SCHEMA, name="AgingRequest")
    as_of_date_dt = parse_date(as_of_date) if as_of_date else date.today()
    report = reports_generator.get_accounts_payable_aging(as_of_date_dt)
    return {
        "status": "success",
        "report_type": "Accounts Payable Aging",
        "as_of_date": as_of_date_dt.isoformat(),
        "company_info": authenticator.get_company_info(),
        "data": report
    }

def _generate_sales_by_customer_report(start_date: str | None, end_date: str | None) -> dict[str, Any]:
    _ensure_authenticated_and_handle_errors()
    input_dict = {
        "period": {"start_date": start_date, "end_date": end_date}
    }
    validate_json_schema(input_dict, SALES_CUSTOMER_REQUEST_SCHEMA, name="SalesCustomerRequest")
    period = create_report_period(start_date, end_date)
    report = reports_generator.get_sales_by_customer(period)
    return {
        "status": "success",
        "report_type": "Sales by Customer",
        "period": {
            "start_date": period.start_date.isoformat(),
            "end_date": period.end_date.isoformat()
        },
        "company_info": authenticator.get_company_info(),
        "data": report
    }

def _generate_expenses_by_vendor_report(start_date: str | None, end_date: str | None) -> dict[str, Any]:
    _ensure_authenticated_and_handle_errors()
    input_dict = {
        "period": {"start_date": start_date, "end_date": end_date}
    }
    validate_json_schema(input_dict, EXPENSES_VENDOR_REQUEST_SCHEMA, name="ExpensesVendorRequest")
    period = create_report_period(start_date, end_date)
    report = reports_generator.get_expenses_by_vendor(period)
    return {
        "status": "success",
        "report_type": "Expenses by Vendor",
        "period": {
            "start_date": period.start_date.isoformat(),
            "end_date": period.end_date.isoformat()
        },
        "company_info": authenticator.get_company_info(),
        "data": report
    }

# Tool registration

def register_tools(mcp: FastMCP):
    @mcp.tool()
    def generate_profit_loss_report(
        start_date: Annotated[str | None, Field(description="Start date in YYYY-MM-DD format. If None, defaults to first day of current month.")] = None,
        end_date: Annotated[str | None, Field(description="End date in YYYY-MM-DD format. If None, defaults to last day of current month.")] = None,
        summarize_by: Annotated[str, Field(description="How to summarize columns. Options: 'Month', 'Quarter', 'Year'. Defaults to 'Month'.")] = "Month"
    ) -> dict[str, Any]:
        try:
            return _generate_profit_loss_report(start_date, end_date, summarize_by)
        except ValueError as e:
            logger.error(f"Error in generate_profit_loss_report: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def generate_balance_sheet_report(
        as_of_date: Annotated[str | None, Field(description="Date in YYYY-MM-DD format. If None, defaults to today's date.")] = None,
        summarize_by: Annotated[str, Field(description="How to summarize columns. Options: 'Month', 'Quarter', 'Year'. Defaults to 'Month'.")] = "Month"
    ) -> dict[str, Any]:
        try:
            return _generate_balance_sheet_report(as_of_date, summarize_by)
        except ValueError as e:
            logger.error(f"Error in generate_balance_sheet_report: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def generate_cash_flow_report(
        start_date: Annotated[str | None, Field(description="Start date in YYYY-MM-DD format. If None, defaults to first day of current month.")] = None,
        end_date: Annotated[str | None, Field(description="End date in YYYY-MM-DD format. If None, defaults to last day of current month.")] = None
    ) -> dict[str, Any]:
        try:
            return _generate_cash_flow_report(start_date, end_date)
        except ValueError as e:
            logger.error(f"Error in generate_cash_flow_report: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def generate_ar_aging_report(
        as_of_date: Annotated[str | None, Field(description="Date in YYYY-MM-DD format. If None, defaults to today's date.")] = None
    ) -> dict[str, Any]:
        try:
            return _generate_ar_aging_report(as_of_date)
        except ValueError as e:
            logger.error(f"Error in generate_ar_aging_report: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def generate_ap_aging_report(
        as_of_date: Annotated[str | None, Field(description="Date in YYYY-MM-DD format. If None, defaults to today's date.")] = None
    ) -> dict[str, Any]:
        try:
            return _generate_ap_aging_report(as_of_date)
        except ValueError as e:
            logger.error(f"Error in generate_ap_aging_report: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def generate_sales_by_customer_report(
        start_date: Annotated[str | None, Field(description="Start date in YYYY-MM-DD format. If None, defaults to first day of current month.")] = None,
        end_date: Annotated[str | None, Field(description="End date in YYYY-MM-DD format. If None, defaults to last day of current month.")] = None
    ) -> dict[str, Any]:
        try:
            return _generate_sales_by_customer_report(start_date, end_date)
        except ValueError as e:
            logger.error(f"Error in generate_sales_by_customer_report: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def generate_expenses_by_vendor_report(
        start_date: Annotated[str | None, Field(description="Start date in YYYY-MM-DD format. If None, defaults to first day of current month.")] = None,
        end_date: Annotated[str | None, Field(description="End date in YYYY-MM-DD format. If None, defaults to last day of current month.")] = None
    ) -> dict[str, Any]:
        try:
            return _generate_expenses_by_vendor_report(start_date, end_date)
        except ValueError as e:
            logger.error(f"Error in generate_expenses_by_vendor_report: {e}")
            return {"status": "error", "message": str(e)}

    # Quick period report tools for common use cases
    @mcp.tool()
    def get_current_month_pl() -> Annotated[dict[str, Any], Field(description="Current month Profit & Loss report data. Returns the same format as generate_profit_loss_report with current month period.")]:
        return _generate_profit_loss_report(
            start_date=get_current_datetime(["year", "month", "day"], first_day_of_month=True),
            end_date=get_current_datetime(["year", "month", "day"], last_day_of_month=True),
            summarize_by="Month"
        )

    @mcp.tool()
    def get_current_quarter_pl() -> Annotated[dict[str, Any], Field(description="Current quarter Profit & Loss report data. Returns the same format as generate_profit_loss_report with current quarter period.")]:
        period = get_current_quarter_period()
        return _generate_profit_loss_report(
            start_date=period.start_date.isoformat(),
            end_date=period.end_date.isoformat(),
            summarize_by="Quarter"
        )

    @mcp.tool()
    def get_current_year_pl() -> Annotated[dict[str, Any], Field(description="Current year Profit & Loss report data. Returns the same format as generate_profit_loss_report with current year period.")]:
        period = get_current_year_period()
        return _generate_profit_loss_report(
            start_date=period.start_date.isoformat(),
            end_date=period.end_date.isoformat(),
            summarize_by="Year"
        )

    @mcp.tool()
    def get_last_month_pl() -> Annotated[dict[str, Any], Field(description="Last month Profit & Loss report data. Returns the same format as generate_profit_loss_report with last month period.")]:
        period = get_last_month_period()
        return _generate_profit_loss_report(
            start_date=period.start_date.isoformat(),
            end_date=period.end_date.isoformat(),
            summarize_by="Month"
        )

    @mcp.tool()
    def get_company_financial_summary() -> Annotated[dict[str, Any], Field(description="Comprehensive financial summary with multiple reports including current month P&L, balance sheet, AR aging, and AP aging. Returns a consolidated report with all key financial metrics.")]:
        try:
            _ensure_authenticated_and_handle_errors()
            # Get current month data
            current_month_pl_period = get_current_month_period()
            current_month_pl = _generate_profit_loss_report(
                start_date=current_month_pl_period.start_date.isoformat(),
                end_date=current_month_pl_period.end_date.isoformat(),
                summarize_by="Month"
            )
            today_str = get_current_datetime(["year", "month", "day"])
            balance_sheet = _generate_balance_sheet_report(as_of_date=today_str, summarize_by="Month")
            ar_aging = _generate_ar_aging_report(as_of_date=today_str)
            ap_aging = _generate_ap_aging_report(as_of_date=today_str)
            return {
                "status": "success",
                "summary_type": "Comprehensive Financial Summary",
                "generated_at": datetime.now().isoformat(),
                "company_info": authenticator.get_company_info(),
                "reports": {
                    "current_month_profit_loss": current_month_pl,
                    "balance_sheet": balance_sheet,
                    "accounts_receivable_aging": ar_aging,
                    "accounts_payable_aging": ap_aging
                }
            }
        except ValueError as e:
            logger.error(f"Error generating financial summary: {e}")
            return {"status": "error", "message": str(e)}


__all__ = [
    "register_tools"
]
