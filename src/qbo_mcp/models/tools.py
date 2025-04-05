# src/qbo_mcp/models/tools.py
from dataclasses import dataclass


@dataclass
class TransactionFilter:
    """Filter criteria for transaction searches."""

    start_date: str | None = None
    end_date: str | None = None
    account_id: str | None = None

    def to_query(self) -> str:
        """Convert filter to QBO query string."""
        query = []

        if self.start_date:
            query.append(f"TxnDate >= '{self.start_date}'")
        if self.end_date:
            query.append(f"TxnDate <= '{self.end_date}'")
        if self.account_id:
            # Assuming account_id is the QBO ID. Adjust if it's the name.
            query.append(f"AccountRef = '{self.account_id}'")

        where_clause = " AND ".join(query) if query else ""
        # Construct the final SELECT query (adjust fields as needed)
        # Example: Selecting basic fields from JournalEntry
        # You might need different queries for different transaction types (Invoice, Bill, etc.)
        # or a more generic Transaction query if available/suitable.
        base_query = "SELECT * FROM JournalEntry" # Placeholder: Adjust based on actual QBO entities
        if where_clause:
            return f"{base_query} WHERE {where_clause}"
        else:
            return base_query

# Add other tool-specific input/output models here as needed.
# For example:
# @dataclass
# class ReportOutput:
#     title: str
#     summary: str
#     data: list[dict] # Or a more specific model