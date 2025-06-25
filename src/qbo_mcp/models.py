"""Pydantic models for tool inputs"""

from pydantic import BaseModel, Field

class ReportPeriodModel(BaseModel):
    """Model for report period input."""
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: str = Field(..., description="End date in YYYY-MM-DD format")


class ProfitLossRequest(BaseModel):
    """Request model for Profit & Loss report."""
    period: ReportPeriodModel | None = Field(None, description="Custom period (defaults to current month)")
    summarize_by: str = Field("Month", description="How to summarize columns (Month, Quarter, Year)")


class BalanceSheetRequest(BaseModel):
    """Request model for Balance Sheet report."""
    as_of_date: str | None = Field(None, description="Date in YYYY-MM-DD format (defaults to today)")
    summarize_by: str = Field("Month", description="How to summarize columns")


class CashFlowRequest(BaseModel):
    """Request model for Cash Flow report."""
    period: ReportPeriodModel | None = Field(None, description="Custom period (defaults to current month)")


class AgingRequest(BaseModel):
    """Request model for aging reports."""
    as_of_date: str | None = Field(None, description="Date in YYYY-MM-DD format (defaults to today)")


class SalesCustomerRequest(BaseModel):
    """Request model for Sales by Customer report."""
    period: ReportPeriodModel | None = Field(None, description="Custom period (defaults to current month)")


class ExpensesVendorRequest(BaseModel):
    """Request model for Expenses by Vendor report."""
    period: ReportPeriodModel | None = Field(None, description="Custom period (defaults to current month)")

__all__ = [
    "ReportPeriodModel",
    "ProfitLossRequest",
    "BalanceSheetRequest",
    "CashFlowRequest",
    "AgingRequest",
    "SalesCustomerRequest",
    "ExpensesVendorRequest"
]