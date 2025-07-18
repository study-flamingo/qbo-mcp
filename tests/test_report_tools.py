import pytest
from unittest.mock import patch
from datetime import date

from qbo_mcp.tools import (
    _generate_profit_loss_report,
    _generate_balance_sheet_report,
    _generate_cash_flow_report,
    _generate_ar_aging_report,
    _generate_ap_aging_report,
    _generate_sales_by_customer_report,
    _generate_expenses_by_vendor_report,
)
from qbo_mcp.reports import ReportPeriod

@pytest.fixture
def mock_dependencies():
    """Pytest fixture to mock dependencies for report generation tests."""
    with patch('qbo_mcp.tools.qbo_service') as mock_qbo_service, \
         patch('qbo_mcp.tools.reports_generator') as mock_reports_generator, \
         patch('qbo_mcp.tools._ensure_authenticated_and_handle_errors') as mock_ensure_auth:
        
        mock_ensure_auth.return_value = None
        mock_qbo_service.get_company_info.return_value = {"CompanyName": "Test Inc."}
        
        yield mock_ensure_auth, mock_reports_generator, mock_qbo_service

def test_generate_profit_loss_report(mock_dependencies):
    """Test the _generate_profit_loss_report function."""
    mock_ensure_auth, mock_reports_generator, mock_qbo_service = mock_dependencies
    
    start_date_str = "2023-01-01"
    end_date_str = "2023-01-31"
    summarize_by = "Month"
    
    mock_reports_generator.get_profit_and_loss.return_value = {"report": "data"}

    result = _generate_profit_loss_report(start_date_str, end_date_str, summarize_by)

    mock_ensure_auth.assert_called_once()
    
    expected_period = ReportPeriod(start_date=date(2023, 1, 1), end_date=date(2023, 1, 31))
    mock_reports_generator.get_profit_and_loss.assert_called_once_with(expected_period, summarize_by)
    
    mock_qbo_service.get_company_info.assert_called_once()

    assert result["status"] == "success"
    assert result["report_type"] == "Profit & Loss"
    assert result["data"] == {"report": "data"}
    assert result["company_info"] == {"CompanyName": "Test Inc."}
    assert result["period"]["start_date"] == start_date_str
    assert result["period"]["end_date"] == end_date_str

def test_generate_balance_sheet_report(mock_dependencies):
    """Test the _generate_balance_sheet_report function."""
    mock_ensure_auth, mock_reports_generator, mock_qbo_service = mock_dependencies

    as_of_date_str = "2023-01-31"
    summarize_by = "Month"
    
    mock_reports_generator.get_balance_sheet.return_value = {"report": "balance_sheet_data"}

    result = _generate_balance_sheet_report(as_of_date_str, summarize_by)

    mock_ensure_auth.assert_called_once()
    
    expected_as_of_date = date(2023, 1, 31)
    mock_reports_generator.get_balance_sheet.assert_called_once_with(expected_as_of_date, summarize_by)
    
    mock_qbo_service.get_company_info.assert_called_once()

    assert result["status"] == "success"
    assert result["report_type"] == "Balance Sheet"
    assert result["data"] == {"report": "balance_sheet_data"}
    assert result["company_info"] == {"CompanyName": "Test Inc."}
    assert result["as_of_date"] == as_of_date_str

def test_generate_cash_flow_report(mock_dependencies):
    """Test the _generate_cash_flow_report function."""
    mock_ensure_auth, mock_reports_generator, mock_qbo_service = mock_dependencies

    start_date_str = "2023-01-01"
    end_date_str = "2023-01-31"
    
    mock_reports_generator.get_cash_flow.return_value = {"report": "cash_flow_data"}

    result = _generate_cash_flow_report(start_date_str, end_date_str)

    mock_ensure_auth.assert_called_once()
    
    expected_period = ReportPeriod(start_date=date(2023, 1, 1), end_date=date(2023, 1, 31))
    mock_reports_generator.get_cash_flow.assert_called_once_with(expected_period)
    
    mock_qbo_service.get_company_info.assert_called_once()

    assert result["status"] == "success"
    assert result["report_type"] == "Cash Flow"
    assert result["data"] == {"report": "cash_flow_data"}
    assert result["company_info"] == {"CompanyName": "Test Inc."}
    assert result["period"]["start_date"] == start_date_str
    assert result["period"]["end_date"] == end_date_str

def test_generate_ar_aging_report(mock_dependencies):
    """Test the _generate_ar_aging_report function."""
    mock_ensure_auth, mock_reports_generator, mock_qbo_service = mock_dependencies

    as_of_date_str = "2023-01-31"
    
    mock_reports_generator.get_accounts_receivable_aging.return_value = {"report": "ar_aging_data"}

    result = _generate_ar_aging_report(as_of_date_str)

    mock_ensure_auth.assert_called_once()
    
    expected_as_of_date = date(2023, 1, 31)
    mock_reports_generator.get_accounts_receivable_aging.assert_called_once_with(expected_as_of_date)
    
    mock_qbo_service.get_company_info.assert_called_once()

    assert result["status"] == "success"
    assert result["report_type"] == "Accounts Receivable Aging"
    assert result["data"] == {"report": "ar_aging_data"}
    assert result["company_info"] == {"CompanyName": "Test Inc."}
    assert result["as_of_date"] == as_of_date_str

def test_generate_ap_aging_report(mock_dependencies):
    """Test the _generate_ap_aging_report function."""
    mock_ensure_auth, mock_reports_generator, mock_qbo_service = mock_dependencies

    as_of_date_str = "2023-01-31"
    
    mock_reports_generator.get_accounts_payable_aging.return_value = {"report": "ap_aging_data"}

    result = _generate_ap_aging_report(as_of_date_str)

    mock_ensure_auth.assert_called_once()
    
    expected_as_of_date = date(2023, 1, 31)
    mock_reports_generator.get_accounts_payable_aging.assert_called_once_with(expected_as_of_date)
    
    mock_qbo_service.get_company_info.assert_called_once()

    assert result["status"] == "success"
    assert result["report_type"] == "Accounts Payable Aging"
    assert result["data"] == {"report": "ap_aging_data"}
    assert result["company_info"] == {"CompanyName": "Test Inc."}
    assert result["as_of_date"] == as_of_date_str

def test_generate_sales_by_customer_report(mock_dependencies):
    """Test the _generate_sales_by_customer_report function."""
    mock_ensure_auth, mock_reports_generator, mock_qbo_service = mock_dependencies
    
    start_date_str = "2023-01-01"
    end_date_str = "2023-01-31"
    
    # Correctly mock the return value
    mock_reports_generator.get_sales_by_customer.return_value = {"report": "sales_data"}

    result = _generate_sales_by_customer_report(start_date_str, end_date_str)

    mock_ensure_auth.assert_called_once()
    
    expected_period = ReportPeriod(start_date=date(2023, 1, 1), end_date=date(2023, 1, 31))
    mock_reports_generator.get_sales_by_customer.assert_called_once_with(expected_period)
    
    mock_qbo_service.get_company_info.assert_called_once()

    assert result["status"] == "success"
    assert result["report_type"] == "Sales by Customer"
    assert result["data"] == {"report": "sales_data"}
    assert result["company_info"] == {"CompanyName": "Test Inc."}
    assert result["period"]["start_date"] == start_date_str
    assert result["period"]["end_date"] == end_date_str

def test_generate_expenses_by_vendor_report(mock_dependencies):
    """Test the _generate_expenses_by_vendor_report function."""
    mock_ensure_auth, mock_reports_generator, mock_qbo_service = mock_dependencies
    
    start_date_str = "2023-01-01"
    end_date_str = "2023-01-31"
    
    mock_reports_generator.get_expenses_by_vendor.return_value = {"report": "expenses_data"}

    result = _generate_expenses_by_vendor_report(start_date_str, end_date_str)

    mock_ensure_auth.assert_called_once()
    
    expected_period = ReportPeriod(start_date=date(2023, 1, 1), end_date=date(2023, 1, 31))
    mock_reports_generator.get_expenses_by_vendor.assert_called_once_with(expected_period)
    
    mock_qbo_service.get_company_info.assert_called_once()

    assert result["status"] == "success"
    assert result["report_type"] == "Expenses by Vendor"
    assert result["data"] == {"report": "expenses_data"}
    assert result["company_info"] == {"CompanyName": "Test Inc."}
    assert result["period"]["start_date"] == start_date_str
    assert result["period"]["end_date"] == end_date_str 