"""QuickBooks Online MCP Server with automatic authentication."""

import logging
from datetime import date, datetime
from typing import Dict, Any, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field

from .models import *
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("qbo-mcp - QuickBooks Online MCP Server")


# Helper functions
def parse_date(date_str: str) -> date:
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def get_report_period(period_model: Optional[ReportPeriodModel]) -> ReportPeriod:
    """Get ReportPeriod from model or default to current month."""
    if period_model:
        return ReportPeriod(
            start_date=parse_date(period_model.start_date),
            end_date=parse_date(period_model.end_date)
        )
    return get_current_month_period()


def ensure_authenticated_response(func):
    """Decorator to ensure authentication before executing report functions."""
    def wrapper(*args, **kwargs):
        try:
            # Check configuration first
            config_errors = config.validate()
            if config_errors:
                return {
                    "status": "error",
                    "message": f"Configuration errors: {', '.join(config_errors)}. Please set up your .env file with QuickBooks app credentials."
                }
            
            # Ensure authentication (will handle OAuth flow if needed)
            if not authenticator.ensure_authenticated():
                return {
                    "status": "error",
                    "message": "Failed to authenticate with QuickBooks Online. Please check your credentials and try again."
                }
            
            # Execute the original function
            return func(*args, **kwargs)
            
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            return {"status": "error", "message": str(e)}
    
    return wrapper


# Report generation tools
@mcp.tool()
@ensure_authenticated_response
def generate_profit_loss_report(request: ProfitLossRequest) -> Dict[str, Any]:
    """
    Generate a Profit & Loss report from QuickBooks Online.
    
    This will automatically handle authentication if needed.
    """
    period = get_report_period(request.period)
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


@mcp.tool()
@ensure_authenticated_response
def generate_balance_sheet_report(request: BalanceSheetRequest) -> Dict[str, Any]:
    """
    Generate a Balance Sheet report from QuickBooks Online.
    
    This will automatically handle authentication if needed.
    """
    as_of_date = parse_date(request.as_of_date) if request.as_of_date else date.today()
    report = reports_generator.get_balance_sheet(as_of_date, request.summarize_by)
    
    return {
        "status": "success",
        "report_type": "Balance Sheet",
        "as_of_date": as_of_date.isoformat(),
        "company_info": authenticator.get_company_info(),
        "data": report
    }


@mcp.tool()
@ensure_authenticated_response
def generate_cash_flow_report(request: CashFlowRequest) -> Dict[str, Any]:
    """
    Generate a Cash Flow statement from QuickBooks Online.
    
    This will automatically handle authentication if needed.
    """
    period = get_report_period(request.period)
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


@mcp.tool()
@ensure_authenticated_response
def generate_ar_aging_report(request: AgingRequest) -> Dict[str, Any]:
    """
    Generate an Accounts Receivable Aging report from QuickBooks Online.
    
    This will automatically handle authentication if needed.
    """
    as_of_date = parse_date(request.as_of_date) if request.as_of_date else date.today()
    report = reports_generator.get_accounts_receivable_aging(as_of_date)
    
    return {
        "status": "success",
        "report_type": "Accounts Receivable Aging",
        "as_of_date": as_of_date.isoformat(),
        "company_info": authenticator.get_company_info(),
        "data": report
    }


@mcp.tool()
@ensure_authenticated_response
def generate_ap_aging_report(request: AgingRequest) -> Dict[str, Any]:
    """
    Generate an Accounts Payable Aging report from QuickBooks Online.
    
    This will automatically handle authentication if needed.
    """
    as_of_date = parse_date(request.as_of_date) if request.as_of_date else date.today()
    report = reports_generator.get_accounts_payable_aging(as_of_date)
    
    return {
        "status": "success",
        "report_type": "Accounts Payable Aging",
        "as_of_date": as_of_date.isoformat(),
        "company_info": authenticator.get_company_info(),
        "data": report
    }


@mcp.tool()
@ensure_authenticated_response
def generate_sales_by_customer_report(request: SalesCustomerRequest) -> Dict[str, Any]:
    """
    Generate a Sales by Customer report from QuickBooks Online.
    
    This will automatically handle authentication if needed.
    """
    period = get_report_period(request.period)
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


@mcp.tool()
@ensure_authenticated_response
def generate_expenses_by_vendor_report(request: ExpensesVendorRequest) -> Dict[str, Any]:
    """
    Generate an Expenses by Vendor report from QuickBooks Online.
    
    This will automatically handle authentication if needed.
    """
    period = get_report_period(request.period)
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


# Quick period report tools for common use cases
@mcp.tool()
def get_current_month_pl() -> Dict[str, Any]:
    """
    Get current month Profit & Loss report (quick access).
    
    This will automatically handle authentication if needed.
    """
    request = ProfitLossRequest(period=None, summarize_by="Month")
    return generate_profit_loss_report(request)


@mcp.tool()
def get_current_quarter_pl() -> Dict[str, Any]:
    """
    Get current quarter Profit & Loss report (quick access).
    
    This will automatically handle authentication if needed.
    """
    period = get_current_quarter_period()
    period_model = ReportPeriodModel(
        start_date=period.start_date.isoformat(),
        end_date=period.end_date.isoformat()
    )
    request = ProfitLossRequest(period=period_model, summarize_by="Quarter")
    return generate_profit_loss_report(request)


@mcp.tool()
def get_current_year_pl() -> Dict[str, Any]:
    """
    Get current year Profit & Loss report (quick access).
    
    This will automatically handle authentication if needed.
    """
    period = get_current_year_period()
    period_model = ReportPeriodModel(
        start_date=period.start_date.isoformat(),
        end_date=period.end_date.isoformat()
    )
    request = ProfitLossRequest(period=period_model, summarize_by="Year")
    return generate_profit_loss_report(request)


@mcp.tool()
def get_last_month_pl() -> Dict[str, Any]:
    """
    Get last month Profit & Loss report (quick access).
    
    This will automatically handle authentication if needed.
    """
    period = get_last_month_period()
    period_model = ReportPeriodModel(
        start_date=period.start_date.isoformat(),
        end_date=period.end_date.isoformat()
    )
    request = ProfitLossRequest(period=period_model, summarize_by="Month")
    return generate_profit_loss_report(request)


@mcp.tool()
def get_company_financial_summary() -> Dict[str, Any]:
    """
    Get a comprehensive financial summary including key reports.
    
    This will automatically handle authentication if needed.
    """
    try:
        # Ensure authentication
        config_errors = config.validate()
        if config_errors:
            return {
                "status": "error",
                "message": f"Configuration errors: {', '.join(config_errors)}"
            }
        
        if not authenticator.ensure_authenticated():
            return {
                "status": "error",
                "message": "Failed to authenticate with QuickBooks Online"
            }
        
        # Get current month data
        current_month_pl = get_current_month_pl()
        balance_sheet = generate_balance_sheet_report(BalanceSheetRequest())
        ar_aging = generate_ar_aging_report(AgingRequest())
        ap_aging = generate_ap_aging_report(AgingRequest())
        
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
        
    except Exception as e:
        logger.error(f"Error generating financial summary: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # Check configuration on startup
    config_errors = config.validate()
    if config_errors:
        print("⚠️  Configuration Issues:")
        for error in config_errors:
            print(f"   - {error}")
        print("\nPlease update your .env file with QuickBooks app credentials.")
        print("See README.md for setup instructions.")
    else:
        print("✅ Configuration validated")
    
    # Run the server
    print("🚀 Starting QuickBooks Online MCP Server...")
    mcp.run()
