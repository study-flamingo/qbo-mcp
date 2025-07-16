# JSON Schemas for MCP tool input validation

REPORT_PERIOD_SCHEMA = {
    "type": "object",
    "properties": {
        "start_date": {"type": "string", "pattern": r"^\\d{4}-\\d{2}-\\d{2}$"},
        "end_date": {"type": "string", "pattern": r"^\\d{4}-\\d{2}-\\d{2}$"}
    },
    "required": ["start_date", "end_date"]
}

PROFIT_LOSS_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "period": REPORT_PERIOD_SCHEMA,
        "summarize_by": {"type": "string"}
    },
    "required": ["period", "summarize_by"]
}

BALANCE_SHEET_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "as_of_date": {"type": "string", "pattern": r"^\\d{4}-\\d{2}-\\d{2}$"},
        "summarize_by": {"type": "string"}
    },
    "required": ["as_of_date", "summarize_by"]
}

CASH_FLOW_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "period": REPORT_PERIOD_SCHEMA
    },
    "required": ["period"]
}

AGING_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "as_of_date": {"type": "string", "pattern": r"^\\d{4}-\\d{2}-\\d{2}$"}
    },
    "required": ["as_of_date"]
}

SALES_CUSTOMER_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "period": REPORT_PERIOD_SCHEMA
    },
    "required": ["period"]
}

EXPENSES_VENDOR_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "period": REPORT_PERIOD_SCHEMA
    },
    "required": ["period"]
}

__all__ = [
    "REPORT_PERIOD_SCHEMA",
    "PROFIT_LOSS_REQUEST_SCHEMA",
    "BALANCE_SHEET_REQUEST_SCHEMA",
    "CASH_FLOW_REQUEST_SCHEMA",
    "AGING_REQUEST_SCHEMA",
    "SALES_CUSTOMER_REQUEST_SCHEMA",
    "EXPENSES_VENDOR_REQUEST_SCHEMA"
] 