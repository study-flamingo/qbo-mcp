# src/qbo_mcp/models/common.py
from dataclasses import dataclass

from intuitlib.client import AuthClient
from quickbooks import QuickBooks


@dataclass
class QBOContext:
    """Context for QuickBooks Online connection."""

    client: QuickBooks
    auth_client: AuthClient