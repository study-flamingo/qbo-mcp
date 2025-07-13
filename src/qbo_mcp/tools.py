import logging
from datetime import date, datetime
from typing import Any
from fastmcp.server import FastMCP

from .auth import authenticator
from .models import *
from .config import config
from .reports import (
    reports_generator,
    ReportPeriod,
    get_current_month_period,
    get_current_quarter_period,
    get_current_year_period,
    get_last_month_period
)

logger = logging.getLogger()


# Helper functions
def parse_date(date_str: str) -> date:
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def create_report_period(period_model: ReportPeriodModel | None) -> ReportPeriod:
    """Get ReportPeriod from model or default to current month."""
    if period_model:
        return ReportPeriod(
            start_date=parse_date(period_model.start_date),
            end_date=parse_date(period_model.end_date)
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


def register_tools(mcp: FastMCP):
    # Report generation tools
    @mcp.tool()
    def generate_profit_loss_report(request: ProfitLossRequest) -> dict[str, Any]:
        """
        Generate a Profit & Loss report from QuickBooks Online.
        """
        try:
            _ensure_authenticated_and_handle_errors()
            period = create_report_period(request.period)
            report = reports_generator.get_profit_and_loss(period, request.summarize_by)
            
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
        except ValueError as e:
            logger.error(f"Error in generate_profit_loss_report: {e}")
            return {"status": "error", "message": str(e)}


    @mcp.tool()
    def generate_balance_sheet_report(request: BalanceSheetRequest) -> dict[str, Any]:
        """
        Generate a Balance Sheet report from QuickBooks Online.
        """
        try:
            _ensure_authenticated_and_handle_errors()
            as_of_date = parse_date(request.as_of_date) if request.as_of_date else date.today()
            report = reports_generator.get_balance_sheet(as_of_date, request.summarize_by)
            
            return {
                "status": "success",
                "report_type": "Balance Sheet",
                "as_of_date": as_of_date.isoformat(),
                "company_info": authenticator.get_company_info(),
                "data": report
            }
        except ValueError as e:
            logger.error(f"Error in generate_balance_sheet_report: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def generate_cash_flow_report(request: CashFlowRequest) -> dict[str, Any]:
        """
        Generate a Cash Flow statement from QuickBooks Online.
        """
        try:
            _ensure_authenticated_and_handle_errors()
            period = create_report_period(request.period)
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
        except ValueError as e:
            logger.error(f"Error in generate_cash_flow_report: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def generate_ar_aging_report(request: AgingRequest) -> dict[str, Any]:
        """
        Generate an Accounts Receivable Aging report from QuickBooks Online.
        """
        try:
            _ensure_authenticated_and_handle_errors()
            as_of_date = parse_date(request.as_of_date) if request.as_of_date else date.today()
            report = reports_generator.get_accounts_receivable_aging(as_of_date)
            
            return {
                "status": "success",
                "report_type": "Accounts Receivable Aging",
                "as_of_date": as_of_date.isoformat(),
                "company_info": authenticator.get_company_info(),
                "data": report
            }
        except ValueError as e:
            logger.error(f"Error in generate_ar_aging_report: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def generate_ap_aging_report(request: AgingRequest) -> dict[str, Any]:
        """
        Generate an Accounts Payable Aging report from QuickBooks Online.
        """
        try:
            _ensure_authenticated_and_handle_errors()
            as_of_date = parse_date(request.as_of_date) if request.as_of_date else date.today()
            report = reports_generator.get_accounts_payable_aging(as_of_date)
            
            return {
                "status": "success",
                "report_type": "Accounts Payable Aging",
                "as_of_date": as_of_date.isoformat(),
                "company_info": authenticator.get_company_info(),
                "data": report
            }
        except ValueError as e:
            logger.error(f"Error in generate_ap_aging_report: {e}")
            return {"status": "error", "message": str(e)}


    @mcp.tool()
    def generate_sales_by_customer_report(request: SalesCustomerRequest) -> dict[str, Any]:
        """
        Generate a Sales by Customer report from QuickBooks Online.
        """
        try:
            _ensure_authenticated_and_handle_errors()
            period = create_report_period(request.period)
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
        except ValueError as e:
            logger.error(f"Error in generate_sales_by_customer_report: {e}")
            return {"status": "error", "message": str(e)}


    @mcp.tool()
    def generate_expenses_by_vendor_report(request: ExpensesVendorRequest) -> dict[str, Any]:
        """
        Generate an Expenses by Vendor report from QuickBooks Online.
        """
        try:
            _ensure_authenticated_and_handle_errors()
            period = create_report_period(request.period)
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
        except ValueError as e:
            logger.error(f"Error in generate_expenses_by_vendor_report: {e}")
            return {"status": "error", "message": str(e)}


    # Quick period report tools for common use cases
    @mcp.tool()
    def get_current_month_pl() -> dict[str, Any]:
        """
        Get current month Profit & Loss report (quick access).
        """
        try:
            _ensure_authenticated_and_handle_errors()
            period = get_current_month_period()
            report = reports_generator.get_profit_and_loss(period, "Month")
            
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
        except ValueError as e:
            logger.error(f"Error in get_current_month_pl: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def get_current_quarter_pl() -> dict[str, Any]:
        """
        Get current quarter Profit & Loss report (quick access).
        """
        try:
            _ensure_authenticated_and_handle_errors()
            period = get_current_quarter_period()
            report = reports_generator.get_profit_and_loss(period, "Quarter")
            
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
        except ValueError as e:
            logger.error(f"Error in get_current_quarter_pl: {e}")
            return {"status": "error", "message": str(e)}


    @mcp.tool()
    def get_current_year_pl() -> dict[str, Any]:
        """
        Get current year Profit & Loss report (quick access).
        """
        try:
            _ensure_authenticated_and_handle_errors()
            period = get_current_year_period()
            report = reports_generator.get_profit_and_loss(period, "Year")
            
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
        except ValueError as e:
            logger.error(f"Error in get_current_year_pl: {e}")
            return {"status": "error", "message": str(e)}


    @mcp.tool()
    def get_last_month_pl() -> dict[str, Any]:
        """
        Get last month Profit & Loss report (quick access).
        """
        try:
            _ensure_authenticated_and_handle_errors()
            period = get_last_month_period()
            report = reports_generator.get_profit_and_loss(period, "Month")
            
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
        except ValueError as e:
            logger.error(f"Error in get_last_month_pl: {e}")
            return {"status": "error", "message": str(e)}


    @mcp.tool()
    def get_company_financial_summary() -> dict[str, Any]:
        """
        Get a comprehensive financial summary including key reports.
        """
        try:
            _ensure_authenticated_and_handle_errors()
            
            # Get current month data
            current_month_pl_period = get_current_month_period()
            current_month_pl = reports_generator.get_profit_and_loss(current_month_pl_period, "Month")

            balance_sheet_request = BalanceSheetRequest()
            balance_sheet_as_of_date = parse_date(balance_sheet_request.as_of_date) if balance_sheet_request.as_of_date else date.today()
            balance_sheet = reports_generator.get_balance_sheet(balance_sheet_as_of_date, balance_sheet_request.summarize_by)

            ar_aging_request = AgingRequest()
            ar_aging_as_of_date = parse_date(ar_aging_request.as_of_date) if ar_aging_request.as_of_date else date.today()
            ar_aging = reports_generator.get_accounts_receivable_aging(ar_aging_as_of_date)

            ap_aging_request = AgingRequest()
            ap_aging_as_of_date = parse_date(ap_aging_request.as_of_date) if ap_aging_request.as_of_date else date.today()
            ap_aging = reports_generator.get_accounts_payable_aging(ap_aging_as_of_date)
            
            return {
                "status": "success",
                "summary_type": "Comprehensive Financial Summary",
                "generated_at": datetime.now().isoformat(),
                "company_info": authenticator.get_company_info(),
                "reports": {
                    "current_month_profit_loss": {
                        "status": "success",
                        "report_type": "Profit & Loss",
                        "period": {
                            "start_date": current_month_pl_period.start_date.isoformat(),
                            "end_date": current_month_pl_period.end_date.isoformat()
                        },
                        "company_info": authenticator.get_company_info(),
                        "data": current_month_pl
                    },
                    "balance_sheet": {
                        "status": "success",
                        "report_type": "Balance Sheet",
                        "as_of_date": balance_sheet_as_of_date.isoformat(),
                        "company_info": authenticator.get_company_info(),
                        "data": balance_sheet
                    },
                    "accounts_receivable_aging": {
                        "status": "success",
                        "report_type": "Accounts Receivable Aging",
                        "as_of_date": ar_aging_as_of_date.isoformat(),
                        "company_info": authenticator.get_company_info(),
                        "data": ar_aging
                    },
                    "accounts_payable_aging": {
                        "status": "success",
                        "report_type": "Accounts Payable Aging",
                        "as_of_date": ap_aging_as_of_date.isoformat(),
                        "company_info": authenticator.get_company_info(),
                        "data": ap_aging
                    }
                }
            }
            
        except ValueError as e:
            logger.error(f"Error generating financial summary: {e}")
            return {"status": "error", "message": str(e)}


__all__ = [
    "register_tools"
]
