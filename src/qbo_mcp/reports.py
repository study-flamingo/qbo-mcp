"""Reports module for generating QuickBooks Online reports."""

import logging
from datetime import datetime, date, timedelta
from dataclasses import dataclass

from quickbooks import QuickBooks
from quickbooks.objects import Account, Item, Customer, Vendor

from .auth import authenticator

logger = logging.getLogger("qbo_mcp")



@dataclass
class ReportPeriod:
    """Represents a reporting period with start and end dates."""
    start_date: date
    end_date: date
    
    def to_qb_format(self) -> dict[str, str]:
        """Convert to QuickBooks API format."""
        return {
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d")
        }


class QBOReportsGenerator:
    """Generates various QuickBooks Online reports."""
    
    def __init__(self, qb_client: QuickBooks | None = None):
        """Initialize with optional QuickBooks client."""
        self.qb_client = qb_client
    
    def _get_client(self) -> QuickBooks:
        """Get authenticated QuickBooks client."""
        if self.qb_client:
            return self.qb_client
        
        client = authenticator.get_authenticated_client()
        if not client:
            raise ValueError("Failed to authenticate with QuickBooks Online")
        return client
    
    def get_profit_and_loss(self, period: ReportPeriod,
                           summarize_column_by: str = "Month") -> dict[str, any]:
        """
        Generate Profit & Loss report.
        
        Args:
            period: Reporting period
            summarize_column_by: How to summarize columns (Month, Quarter, Year, etc.)
        """
        try:
            client = self._get_client()
            
            # Build report parameters
            params = {
                "summarize_column_by": summarize_column_by,
                **period.to_qb_format()
            }
            
            # Get P&L report from QuickBooks
            report_data = client.get_report("ProfitAndLoss", params)
            
            # Process and structure the report data
            processed_report = self._process_profit_loss_report(report_data)
            
            logger.info(f"Generated P&L report for {period.start_date} to {period.end_date}")
            return processed_report
            
        except Exception as e:
            logger.error(f"Error generating P&L report: {e}")
            raise
    
    def get_balance_sheet(self, as_of_date: date,
                         summarize_column_by: str = "Month") -> dict[str, any]:
        """
        Generate Balance Sheet report.
        
        Args:
            as_of_date: Date for the balance sheet
            summarize_column_by: How to summarize columns
        """
        try:
            client = self._get_client()
            
            params = {
                "summarize_column_by": summarize_column_by,
                "end_date": as_of_date.strftime("%Y-%m-%d")
            }
            
            report_data = client.get_report("BalanceSheet", params)
            processed_report = self._process_balance_sheet_report(report_data)
            
            logger.info(f"Generated Balance Sheet as of {as_of_date}")
            return processed_report
            
        except Exception as e:
            logger.error(f"Error generating Balance Sheet: {e}")
            raise
    
    def get_cash_flow(self, period: ReportPeriod) -> dict[str, any]:
        """
        Generate Cash Flow statement.
        
        Args:
            period: Reporting period
        """
        try:
            client = self._get_client()
            
            params = period.to_qb_format()
            report_data = client.get_report("CashFlow", params)
            processed_report = self._process_cash_flow_report(report_data)
            
            logger.info(f"Generated Cash Flow for {period.start_date} to {period.end_date}")
            return processed_report
            
        except Exception as e:
            logger.error(f"Error generating Cash Flow report: {e}")
            raise
    
    def get_accounts_receivable_aging(self, as_of_date: date | None = None) -> dict[str, any]:
        """
        Generate Accounts Receivable Aging report.
        
        Args:
            as_of_date: Date for aging report (defaults to today)
        """
        try:
            client = self._get_client()
            
            if as_of_date is None:
                as_of_date = date.today()
            
            params = {
                "end_date": as_of_date.strftime("%Y-%m-%d")
            }
            
            report_data = client.get_report("AgedReceivables", params)
            processed_report = self._process_aging_report(report_data, "receivables")
            
            logger.info(f"Generated A/R Aging as of {as_of_date}")
            return processed_report
            
        except Exception as e:
            logger.error(f"Error generating A/R Aging report: {e}")
            raise
    
    def get_accounts_payable_aging(self, as_of_date: date | None = None) -> dict[str, any]:
        """
        Generate Accounts Payable Aging report.
        
        Args:
            as_of_date: Date for aging report (defaults to today)
        """
        try:
            client = self._get_client()
            
            if as_of_date is None:
                as_of_date = date.today()
            
            params = {
                "end_date": as_of_date.strftime("%Y-%m-%d")
            }
            
            report_data = client.get_report("AgedPayables", params)
            processed_report = self._process_aging_report(report_data, "payables")
            
            logger.info(f"Generated A/P Aging as of {as_of_date}")
            return processed_report
            
        except Exception as e:
            logger.error(f"Error generating A/P Aging report: {e}")
            raise
    
    def get_sales_by_customer(self, period: ReportPeriod) -> dict[str, any]:
        """
        Generate Sales by Customer report.
        
        Args:
            period: Reporting period
        """
        try:
            client = self._get_client()
            
            params = period.to_qb_format()
            report_data = client.get_report("CustomerSales", params)
            processed_report = self._process_sales_report(report_data)
            
            logger.info(f"Generated Sales by Customer for {period.start_date} to {period.end_date}")
            return processed_report
            
        except Exception as e:
            logger.error(f"Error generating Sales by Customer report: {e}")
            raise
    
    def get_expenses_by_vendor(self, period: ReportPeriod) -> dict[str, any]:
        """
        Generate Expenses by Vendor report.
        
        Args:
            period: Reporting period
        """
        try:
            client = self._get_client()
            
            params = period.to_qb_format()
            report_data = client.get_report("VendorExpenses", params)
            processed_report = self._process_expenses_report(report_data)
            
            logger.info(f"Generated Expenses by Vendor for {period.start_date} to {period.end_date}")
            return processed_report
            
        except Exception as e:
            logger.error(f"Error generating Expenses by Vendor report: {e}")
            raise
    
    def _process_profit_loss_report(self, report_data: dict[str, any]) -> dict[str, any]:
        """Process raw P&L report data into structured format."""
        try:
            header = report_data.get("Header", {})
            rows = report_data.get("Rows", [])
            
            processed = {
                "report_name": header.get("ReportName", "Profit and Loss"),
                "report_basis": header.get("ReportBasis", "Accrual"),
                "start_period": header.get("StartPeriod"),
                "end_period": header.get("EndPeriod"),
                "currency": header.get("Currency", "USD"),
                "sections": {}
            }
            
            current_section = None
            
            for row in rows:
                if row.get("type") == "Section":
                    section_data = row.get("group", [])
                    if section_data:
                        section_name = section_data[0].get("value", "Unknown Section")
                        current_section = section_name
                        processed["sections"][current_section] = {
                            "items": [],
                            "subtotal": 0
                        }
                
                elif row.get("type") == "Data" and current_section:
                    row_data = row.get("group", [])
                    if len(row_data) >= 2:
                        account_name = row_data[0].get("value", "")
                        amount = self._parse_amount(row_data[1].get("value", "0"))
                        
                        processed["sections"][current_section]["items"].append({
                            "account": account_name,
                            "amount": amount
                        })
            
            # Calculate subtotals
            for section in processed["sections"].values():
                section["subtotal"] = sum(item["amount"] for item in section["items"])
            
            return processed
            
        except Exception as e:
            logger.error(f"Error processing P&L report: {e}")
            return {"error": str(e), "raw_data": report_data}
    
    def _process_balance_sheet_report(self, report_data: dict[str, any]) -> dict[str, any]:
        """Process raw Balance Sheet report data."""
        # Similar structure to P&L processing
        return self._process_profit_loss_report(report_data)
    
    def _process_cash_flow_report(self, report_data: dict[str, any]) -> dict[str, any]:
        """Process raw Cash Flow report data."""
        return self._process_profit_loss_report(report_data)
    
    def _process_aging_report(self, report_data: dict[str, any] | None, report_type: str) -> dict[str, any]:
        """Process aging report data (A/R or A/P)."""
        if report_data is None:
            return {"error": "No report data provided", "report_type": report_type}
        try:
            header = report_data.get("Header", {})
            rows = report_data.get("Rows", [])
            
            processed = {
                "report_name": header.get("ReportName", f"{report_type.title()} Aging"),
                "as_of_date": header.get("EndPeriod"),
                "currency": header.get("Currency", "USD"),
                "aging_buckets": [],
                "customers_vendors": []
            }
            
            for row in rows:
                if row.get("type") == "Data":
                    row_data = row.get("group", [])
                    if len(row_data) >= 6:  # Typical aging report has 6+ columns
                        entity_name = row_data[0].get("value", "")
                        current = self._parse_amount(row_data[1].get("value", "0"))
                        days_1_30 = self._parse_amount(row_data[2].get("value", "0"))
                        days_31_60 = self._parse_amount(row_data[3].get("value", "0"))
                        days_61_90 = self._parse_amount(row_data[4].get("value", "0"))
                        over_90 = self._parse_amount(row_data[5].get("value", "0"))
                        total = sum([current, days_1_30, days_31_60, days_61_90, over_90])
                        
                        processed["customers_vendors"].append({
                            "name": entity_name,
                            "current": current,
                            "1_30_days": days_1_30,
                            "31_60_days": days_31_60,
                            "61_90_days": days_61_90,
                            "over_90_days": over_90,
                            "total": total
                        })
            return processed
        except Exception as e:
            logger.error(f"Error processing aging report: {e}")
            return {"error": str(e), "raw_data": report_data}
    
    def _process_sales_report(self, report_data: dict[str, any]) -> dict[str, any]:
        """Process sales by customer report data."""
        return self._process_profit_loss_report(report_data)
    
    def _process_expenses_report(self, report_data: dict[str, any]) -> dict[str, any]:
        """Process expenses by vendor report data."""
        return self._process_profit_loss_report(report_data)
    
    def _parse_amount(self, amount_str: str) -> float:
        """Parse amount string to float, handling various formats."""
        if not amount_str or amount_str in ["", "-"]:
            return 0.0
        
        try:
            # Remove currency symbols, commas, and parentheses
            cleaned = amount_str.replace("$", "").replace(",", "").replace("(", "-").replace(")", "")
            return float(cleaned)
        except (ValueError, TypeError):
            return 0.0


# Utility functions for common reporting periods
def get_current_month_period() -> ReportPeriod:
    """Get current month reporting period."""
    today = date.today()
    start_of_month = date(today.year, today.month, 1)
    return ReportPeriod(start_of_month, today)


def get_current_quarter_period() -> ReportPeriod:
    """Get current quarter reporting period."""
    today = date.today()
    quarter = (today.month - 1) // 3 + 1
    start_month = (quarter - 1) * 3 + 1
    start_of_quarter = date(today.year, start_month, 1)
    return ReportPeriod(start_of_quarter, today)


def get_current_year_period() -> ReportPeriod:
    """Get current year reporting period."""
    today = date.today()
    start_of_year = date(today.year, 1, 1)
    return ReportPeriod(start_of_year, today)


def get_last_month_period() -> ReportPeriod:
    """Get last month reporting period."""
    today = date.today()
    if today.month == 1:
        last_month = date(today.year - 1, 12, 1)
        end_date = date(today.year, 1, 1) - timedelta(days=1)
    else:
        last_month = date(today.year, today.month - 1, 1)
        end_date = date(today.year, today.month, 1) - timedelta(days=1)
    
    return ReportPeriod(last_month, end_date)


# Global reports generator instance
reports_generator = QBOReportsGenerator()
