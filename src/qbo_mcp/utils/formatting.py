# src/qbo_mcp/utils/formatting.py
"""
Utility functions for formatting data and errors for the MCP server.
"""
import logging

# Import QuickbooksException if needed for type checking, adjust path as necessary
# from quickbooks.exceptions import QuickbooksException

logger = logging.getLogger(__name__)

def format_qbo_error(e: Exception) -> str:
    """
    Formats QuickBooks and other exceptions into user-friendly error messages.
    Logs the detailed error internally.
    """
    # Check if it's a Quickbooks specific exception first (requires import)
    # if isinstance(e, QuickbooksException):
    #     logger.error(f"QuickBooks API Error: {e}", exc_info=True)
    #     # You might want to extract more specific details from QuickbooksException if available
    #     return f"QuickBooks error: {str(e)}"
    # else:
    #     logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    #     return f"An unexpected error occurred: {str(e)}"

    # Simplified version without specific QuickbooksException check for now
    logger.error(f"Error during QBO operation: {e}", exc_info=True)
    return f"An error occurred while communicating with QuickBooks: {str(e)}"

# Add other formatting functions here if needed, e.g., for formatting report data.