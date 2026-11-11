# QBO Payments API — Evaluation

Question (Dr. Joel): *Should we implement the QBO Payments API? Would it let us
programmatically categorize transactions, change settings, etc.?*

Short answer: **No — the Payments API is for *taking* money, not for
categorizing or configuring the books.** The capabilities you're describing
belong to the **Accounting API**, which we already use. Only add the Payments API
if you specifically need to charge cards / pull ACH programmatically.

---

## 1. Two separate Intuit APIs

| | **Accounting API** (what `qbo-mcp` uses) | **Payments API** |
|---|---|---|
| Purpose | Read/write the books: invoices, bills, payments, journal entries, chart of accounts, reports | Take money: card charges, ACH/eChecks, refunds, tokenization |
| Scope | `com.intuit.quickbooks.accounting` | `com.intuit.quickbooks.payment` |
| Base host | `quickbooks.api.intuit.com` / `…sandbox…` | `api.intuit.com` (payments host; `/quickbooks/v4/payments/…`) |
| Where data lands | QuickBooks Online company file (UI/reports) | **Merchant Center** (merchant account) |
| Records a bookkeeping txn? | Yes | **No** — must be recorded separately via Accounting API |
| Requires | QBO company + app | **A QuickBooks Payments merchant account** (underwriting/eligibility) |

Key consequence: a payment taken via the Payments API **does not automatically
create a Sales Receipt / Payment in the books** — Intuit's own guidance is to use
the two APIs together: Payments API to charge, Accounting API to record/categorize.

## 2. Capability matrix

| Capability | Accounting API | Payments API |
|---|---|---|
| Categorize a bank/CC transaction (assign account) | ✅ update the txn's line `AccountRef` (Purchase, Deposit, JournalEntry, Transfer, Payment…) | ❌ |
| Create/edit invoices, bills, payments, sales receipts | ✅ | ❌ |
| Journal entries / reclass | ✅ | ❌ |
| Chart of accounts CRUD | ✅ | ❌ |
| Change company/accounting **settings** | ⚠️ limited — `Preferences` entity is mostly read-only; a handful of fields writable | ❌ |
| Read/write customers, vendors, items | ✅ | ❌ |
| Reports (P&L, Balance Sheet, Aging, …) | ✅ (reports endpoint) | ❌ |
| Charge a credit card | ❌ | ✅ Charges + Cards |
| ACH / eCheck payment | ❌ | ✅ Bank accounts / eChecks |
| Refund | ❌ (as accounting refund receipt only) | ✅ Refunds |
| Tokenize a card for later | ❌ | ✅ Tokens |
| List merchant transactions | ❌ | ✅ (Merchant Center data) |

### On "programmatically categorize transactions"
Categorization is an accounting operation. With the **Accounting API** you can:
- Read uncategorized bank/CC transactions and update their line detail to point
  at an `AccountRef` (this is the "categorize" action).
- Create `JournalEntry`/`Transfer`/`Purchase`/`Deposit` objects with explicit
  account refs.
- Batch operations (QBO `batch` endpoint, up to 30 ops/request).

This is a natural extension of the existing tool set — no Payments API needed.

### On "change other settings"
Limited. The `Preferences` entity covers sales-tax, currency, and other prefs but
is **largely read-only** via API; most admin settings (users, subscription,
company profile specifics) are **not** exposed. Set expectations accordingly.

## 3. What implementing the Payments API would take

1. App reconfigured in the Intuit console as **"QuickBooks Online and Payments"**.
2. Add scope `com.intuit.quickbooks.payment`; users must re-consent (new OAuth run).
3. A **Payments merchant account** associated with the QBO company.
4. Separate client/endpoints (different host and path family) — a second service
   class alongside `QBOService`; likely the rest-API via `requests` rather than
   `python-quickbooks`.
5. PCI/security surface: card data, tokens, idempotency keys, webhooks for
   payment status. This is real production weight (not just a new tool function).

## 4. Recommendation

- **If the goal is categorization / bookkeeping automation → skip Payments API.**
  Extend the Accounting API tools instead:
  - `list_transactions` (Purchase/Deposit/JournalEntry, filter by date/account)
  - `categorize_transaction` (sparse-update a line's `AccountRef`)
  - `create_journal_entry` / `create_transfer`
  - Account & preferences read tools
  These are low-risk, reuse the existing auth/reporting plumbing, and stay inside
  the current scope.
- **Only pursue the Payments API** if you genuinely need to accept card/ACH
  payments through your own system (e.g., a payment page or automated billing).
  In that case it's a separate, larger project — do it after the security and
  dependency work above, with webhooks and idempotency designed up front.

### Phased suggestion
1. Hardening (tokens rotated, lazy auth, retries) — in progress.
2. Accounting API write-tools for categorization + a few settings reads.
3. Reassess Payments API need; if yes, scope it as its own initiative.
