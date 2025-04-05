# src/qbo_mcp/api/prompts.py
"""
MCP Prompt definitions for guiding user interactions.
"""
import logging
from datetime import datetime, timedelta

# Import the server instance (assuming it's defined in src/qbo_mcp/server.py)
from ..server import mcp

logger = logging.getLogger(__name__)

# Note: Assumes 'mcp' instance is accessible via import.

@mcp.prompt()
def analyze_cash_flow() -> str:
    """Guide for analyzing cash flow"""
    # This prompt could potentially use tools internally in the future
    return """I'll help you analyze the company's cash flow situation. I'll:

1. Review the current balance sheet to assess cash position and working capital
2. Check aged receivables to understand collection status
3. Identify any concerning trends or potential cash flow issues
4. Provide specific recommendations for improving cash flow

Would you like me to proceed with this analysis?"""


@mcp.prompt()
def monthly_review() -> str:
    """Guide for monthly financial review"""
    try:
        today = datetime.now()
        first_of_month = today.replace(day=1)
        last_month_end = first_of_month - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)

        start_str = last_month_start.strftime("%B %d, %Y") # Use a clear format
        end_str = last_month_end.strftime("%B %d, %Y")

        return f"""I'll help you review the financial results for last month ({start_str} - {end_str}). I'll:

1. Analyze the P&L statement from {start_str} to {end_str}
2. Review the balance sheet as of {end_str}
3. Highlight key metrics and significant changes
4. Identify areas that need attention
5. Suggest specific actions for improvement

Would you like me to proceed with this review?"""
    except Exception as e:
        logger.error(f"Error generating monthly review prompt dates: {e}")
        # Fallback prompt if date calculation fails
        return """I can help you review the financial results for the previous month.
Would you like me to proceed?"""


@mcp.prompt()
def accounts_receivable_analysis() -> str:
    """Guide for AR analysis"""
    return """I'll help you analyze the accounts receivable situation. I'll:

1. Review the aged receivables report
2. Identify overdue accounts and aging patterns
3. Calculate key collection metrics
4. Recommend specific strategies for improving collections

Would you like me to proceed with this analysis?"""