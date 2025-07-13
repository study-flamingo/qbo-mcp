"""Pydantic models for tool inputs"""

from pydantic import BaseModel, Field, field_validator
from datetime import time, datetime, timedelta


# Helper function to get current date and time in a specific format
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
        str: Current date and time formatted as a string. *("YYYY-MM-DD HH:MM:SS")*"""
    current_dt = datetime.now()

    if last_day_of_month:
        # Calculate the last day of the current month
        # Go to the first day of the next month and subtract one day
        next_month = current_dt.replace(day=28) + timedelta(days=4) # this will never fail
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


class ReportPeriodModel(BaseModel):
    """Model for report period input."""
    start_date: str = Field(default_factory=lambda: get_current_datetime(include=["year", "month", "day"], first_day_of_month=True), description="Start date in YYYY-MM-DD format")
    end_date: str = Field(default_factory=lambda: get_current_datetime(include=["year", "month", "day"], last_day_of_month=True), description="End date in YYYY-MM-DD format")

    @field_validator('start_date', 'end_date', mode='before')
    def convert_datetime_to_str(cls, v):
        if isinstance(v, datetime):
            return v.strftime("%Y-%m-%d")
        return v

    @classmethod
    def from_strings(cls, start_date: str | None = None, end_date: str | None = None) -> "ReportPeriodModel":
        """
        Constructs a ReportPeriodModel from string dates.
        Dates should be in YYYY-MM-DD format.
        """
        if not start_date:
            start_date = get_current_datetime(include=["year", "month", "day"], first_day_of_month=True)
        if not end_date:
            end_date = get_current_datetime(include=["year", "month", "day"], last_day_of_month=True)
        return cls(start_date=start_date, end_date=end_date)


class ProfitLossRequest(BaseModel):
    """Request model for Profit & Loss report."""
    period: ReportPeriodModel | None = Field(..., description="Custom period (defaults to current month)")
    summarize_by: str = Field("Month", description="How to summarize columns (Month, Quarter, Year)")

    @classmethod
    def from_strings(cls, start_date: str | None = None, end_date: str | None = None, summarize_by: str = "Month") -> "ProfitLossRequest":
        period = ReportPeriodModel.from_strings(start_date=start_date, end_date=end_date)
        return cls(period=period, summarize_by=summarize_by)


class BalanceSheetRequest(BaseModel):
    """Request model for Balance Sheet report."""
    as_of_date: str = Field(default_factory=lambda: get_current_datetime(include=["year", "month", "day"]), description="Date in YYYY-MM-DD format (defaults to today)")
    summarize_by: str = Field(default="Month", description="How to summarize columns")

    @classmethod
    def from_strings(cls, as_of_date: str | None = None, summarize_by: str = "Month") -> "BalanceSheetRequest":
        if as_of_date is None:
            as_of_date = get_current_datetime(include=["year", "month", "day"])
        return cls(as_of_date=as_of_date, summarize_by=summarize_by)


class CashFlowRequest(BaseModel):
    """Request model for Cash Flow report."""
    period: ReportPeriodModel | None = Field(None, description="Custom period (defaults to current month)")

    @classmethod
    def from_strings(cls, start_date: str | None = None, end_date: str | None = None) -> "CashFlowRequest":
        period = ReportPeriodModel.from_strings(start_date=start_date, end_date=end_date)
        return cls(period=period)


class AgingRequest(BaseModel):
    """Request model for aging reports."""
    as_of_date: str = Field(default_factory=lambda: get_current_datetime(include=["year", "month", "day"]), description="Date in YYYY-MM-DD format (defaults to today)")

    @classmethod
    def from_strings(cls, as_of_date: str | None = None) -> "AgingRequest":
        if as_of_date is None:
            as_of_date = get_current_datetime(include=["year", "month", "day"])
        return cls(as_of_date=as_of_date)


class SalesCustomerRequest(BaseModel):
    """Request model for Sales by Customer report."""
    period: ReportPeriodModel | None = Field(None, description="Custom period (defaults to current month)")

    @classmethod
    def from_strings(cls, start_date: str | None = None, end_date: str | None = None) -> "SalesCustomerRequest":
        period = ReportPeriodModel.from_strings(start_date=start_date, end_date=end_date)
        return cls(period=period)


class ExpensesVendorRequest(BaseModel):
    """Request model for Expenses by Vendor report."""
    period: ReportPeriodModel | None = Field(None, description="Custom period (defaults to current month)")

    @classmethod
    def from_strings(cls, start_date: str | None = None, end_date: str | None = None) -> "ExpensesVendorRequest":
        period = ReportPeriodModel.from_strings(start_date=start_date, end_date=end_date)
        return cls(period=period)


__all__ = [
    "ReportPeriodModel",
    "ProfitLossRequest",
    "BalanceSheetRequest",
    "CashFlowRequest",
    "AgingRequest",
    "SalesCustomerRequest",
    "ExpensesVendorRequest"
]