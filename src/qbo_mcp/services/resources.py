from quickbooks.objects.account import Account
from quickbooks.objects.customer import Customer
from quickbooks.objects.invoice import Invoice

from ..models import QBOContext


def get_accounts(ctx: QBOContext) -> list[Account]:
    """Get list of all accounts."""
    return Account.all(qbo=ctx.client)


def get_customers(ctx: QBOContext) -> list[Customer]:
    """Get list of all customers."""
    return Customer.all(qbo=ctx.client)


def get_recent_invoices(ctx: QBOContext, limit: int = 10) -> list[Invoice]:
    """Get list of recent invoices."""
    return Invoice.filter(
        qbo=ctx.client,
        max_results=limit,
        start_position=1,
    )
