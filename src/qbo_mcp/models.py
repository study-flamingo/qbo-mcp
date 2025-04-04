from dataclasses import dataclass
from typing import Any

from intuitlib.client import AuthClient
from quickbooks import QuickBooks


@dataclass
class QBOContext:
    """Context for QuickBooks Online connection."""

    client: QuickBooks
    auth_client: AuthClient


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
            query.append(f"AccountRef = '{self.account_id}'")

        where_clause = " AND ".join(query) if query else ""
        return where_clause
