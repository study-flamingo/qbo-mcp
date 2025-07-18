import pytest
from datetime import datetime, timedelta, date
from qbo_mcp.tools import (
    get_current_datetime,
    parse_date,
    create_report_period,
    validate_json_schema,
    get_current_month_period
)

def test_get_current_datetime_default():
    """
    Test get_current_datetime with no arguments.
    """
    now = datetime.now()
    expected_format = now.strftime("%Y-%m-%d %H:%M:%S")
    assert get_current_datetime() == expected_format

def test_get_current_datetime_include_year_month():
    """
    Test get_current_datetime with include=['year', 'month'].
    """
    now = datetime.now()
    expected_format = now.strftime("%Y-%m-")
    assert get_current_datetime(include=['year', 'month']) == expected_format.strip()

def test_get_current_datetime_first_day_of_month():
    """
    Test get_current_datetime with first_day_of_month=True.
    """
    now = datetime.now().replace(day=1)
    expected_format = now.strftime("%Y-%m-%d %H:%M:%S")
    assert get_current_datetime(first_day_of_month=True) == expected_format

def test_get_current_datetime_last_day_of_month():
    """
    Test get_current_datetime with last_day_of_month=True.
    """
    now = datetime.now()
    next_month = now.replace(day=28) + timedelta(days=4)
    last_day = next_month - timedelta(days=next_month.day)
    expected_format = last_day.strftime("%Y-%m-%d %H:%M:%S")
    assert get_current_datetime(last_day_of_month=True) == expected_format

def test_parse_date():
    """
    Test the parse_date function.
    """
    assert parse_date("2023-01-15") == date(2023, 1, 15)
    with pytest.raises(ValueError):
        parse_date("invalid-date")

def test_create_report_period():
    """
    Test the create_report_period function.
    """
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    period = create_report_period(start_date, end_date)
    assert period.start_date == date(2023, 1, 1)
    assert period.end_date == date(2023, 1, 31)

def test_create_report_period_defaults():
    """
    Test create_report_period with default values.
    """
    period = create_report_period(None, None)
    expected_period = get_current_month_period()
    assert period.start_date == expected_period.start_date
    assert period.end_date == expected_period.end_date


def test_validate_json_schema_valid():
    """
    Test validate_json_schema with valid data.
    """
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    instance = {"name": "test"}
    try:
        validate_json_schema(instance, schema)
    except ValueError:
        pytest.fail("validate_json_schema raised ValueError unexpectedly!")

def test_validate_json_schema_invalid():
    """
    Test validate_json_schema with invalid data.
    """
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    instance = {"name": 123}
    with pytest.raises(ValueError):
        validate_json_schema(instance, schema, "TestSchema") 