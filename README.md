# QuickBooks Online MCP Server

A Model Context Protocol (MCP) server for integrating with QuickBooks Online, built with FastMCP 2.9. This server provides automatic authentication and comprehensive financial reporting tools.

## ✨ Features

### 🔐 Automatic Authentication
- **Zero-touch OAuth flow** - Authentication handled automatically
- **Browser-based authorization** - Opens browser when auth needed
- **Automatic token management** - Refresh and storage handled behind the scenes
- **Support for sandbox and production** environments

### 📊 Financial Reports
- **Profit & Loss Statement** - Income and expense summary for any period
- **Balance Sheet** - Assets, liabilities, and equity snapshot
- **Cash Flow Statement** - Cash inflows and outflows analysis
- **Accounts Receivable Aging** - Outstanding customer invoices by age
- **Accounts Payable Aging** - Outstanding vendor bills by age
- **Sales by Customer** - Revenue breakdown by customer
- **Expenses by Vendor** - Expense breakdown by vendor
- **Financial Summary** - Comprehensive overview combining key reports

### 🚀 Quick Access Tools
- Current month, quarter, year, and last month P&L reports
- Customizable reporting periods and summarization options

## Prerequisites

1. **QuickBooks Online Developer Account**
   - Sign up at [Intuit Developer](https://developer.intuit.com/)
   - Create a new app to get Client ID and Secret

2. **Python 3.12+**

3. **QuickBooks Online Company**
   - Sandbox company for testing (created automatically)
   - Or production company for live data

## 🛠️ Installation

1. **Setup the project:**
   ```bash
   cd C:/Users/JoelCasimir/Code/Repos/mcp-dev/qbo-mcp
   uv sync
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your QuickBooks app credentials
   ```

3. **Set up your QuickBooks app:**
   - Go to [Intuit Developer Console](https://developer.intuit.com/app/developer/myapps)
   - Create a new app or use existing one
   - **Important**: Add redirect URI: `http://localhost:8080/callback`
   - Note your Client ID and Client Secret

## ⚙️ Configuration

Edit the `.env` file with your QuickBooks app credentials:

```env
# Required - Get from Intuit Developer Console
QBO_CLIENT_ID=your_client_id_here
QBO_CLIENT_SECRET=your_client_secret_here

# OAuth callback URL (must match your app settings exactly)
QBO_REDIRECT_URI=http://localhost:8080/callback

# Environment: sandbox (for testing) or production (for live data)
QBO_ENVIRONMENT=sandbox

# Token storage location
QBO_TOKEN_FILE=qbo_tokens.json
```

## 🚀 Usage

### Running the Server

```bash
# Using uv
uv run qbo-mcp

# Or with activated virtual environment
python -m qbo_mcp
```

### Authentication (Automatic!)

🎉 **No manual auth steps needed!** The server handles everything automatically:

1. **First time**: Browser opens for QuickBooks authorization
2. **Subsequent uses**: Stored tokens are used automatically
3. **Token expiry**: Tokens are refreshed automatically
4. **Re-auth needed**: Browser opens again only if necessary

Just start using the report tools - authentication happens seamlessly in the background!

### 📊 Generating Reports

All report tools automatically handle authentication. Just call the tools you need:

#### Quick Access Reports
```python
# Current month P&L (most common)
get_current_month_pl()

# Current quarter P&L
get_current_quarter_pl()

# Current year P&L
get_current_year_pl()

# Last month P&L
get_last_month_pl()

# Comprehensive financial overview
get_company_financial_summary()
```

#### Detailed Reports with Custom Periods
```python
# P&L for specific period
generate_profit_loss_report({
    "period": {
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    },
    "summarize_by": "Quarter"
})

# Balance Sheet as of specific date
generate_balance_sheet_report({
    "as_of_date": "2024-12-31",
    "summarize_by": "Month"
})

# Cash Flow for custom period
generate_cash_flow_report({
    "period": {
        "start_date": "2024-10-01",
        "end_date": "2024-12-31"
    }
})
```

#### Aging and Analysis Reports
```python
# A/R Aging as of today
generate_ar_aging_report({})

# A/P Aging as of specific date
generate_ap_aging_report({
    "as_of_date": "2024-12-31"
})

# Sales by Customer for current month
generate_sales_by_customer_report({})

# Expenses by Vendor for custom period
generate_expenses_by_vendor_report({
    "period": {
        "start_date": "2024-07-01",
        "end_date": "2024-09-30"
    }
})
```

## 🏗️ Project Structure

```
qbo-mcp/
├── src/qbo_mcp/
│   ├── __init__.py          # Main entry point
│   ├── server.py            # FastMCP server with report tools
│   ├── config.py            # Configuration management
│   ├── auth.py              # Automatic OAuth authentication
│   └── reports.py           # Report generation logic
├── .env.example             # Environment template
├── pyproject.toml           # Project dependencies
└── README.md                # This file
```

## 🔧 Available Tools

| Tool | Description | Quick Use |
|------|-------------|-----------|
| `get_current_month_pl` | Current month P&L | Most common report |
| `get_current_quarter_pl` | Current quarter P&L | Quarterly review |
| `get_current_year_pl` | Current year P&L | Annual analysis |
| `get_last_month_pl` | Last month P&L | Previous month review |
| `get_company_financial_summary` | Complete financial overview | Executive summary |
| `generate_profit_loss_report` | Custom P&L with flexible periods | Custom analysis |
| `generate_balance_sheet_report` | Balance sheet as of any date | Financial position |
| `generate_cash_flow_report` | Cash flow for any period | Liquidity analysis |
| `generate_ar_aging_report` | A/R aging analysis | Collections focus |
| `generate_ap_aging_report` | A/P aging analysis | Payment planning |
| `generate_sales_by_customer_report` | Revenue by customer | Sales analysis |
| `generate_expenses_by_vendor_report` | Expenses by vendor | Vendor analysis |

## 🔒 Security & Best Practices

- **Automatic token management** - No manual token handling needed
- **Secure credential storage** - Environment variables only
- **Sandbox testing** - Use sandbox environment for development
- **Local callback server** - OAuth handled on localhost only
- **Token encryption** - Stored tokens are managed securely

## 🔍 Troubleshooting

### First Setup Issues

**"Configuration errors" on startup:**
```
Solution: Ensure .env file has QBO_CLIENT_ID and QBO_CLIENT_SECRET set
```

**"Failed to authenticate" errors:**
```
1. Check that redirect URI in your QuickBooks app matches: http://localhost:8080/callback
2. Verify Client ID and Secret are correct
3. Ensure you're using the right environment (sandbox vs production)
```

**Browser doesn't open for auth:**
```
1. Check the console for the authorization URL
2. Manually copy and open the URL in your browser
3. Complete the authorization process
```

### Runtime Issues

**"No company data" in reports:**
```
- Sandbox companies start empty - this is normal
- Add sample data in QuickBooks Online sandbox
- Or connect to a production company with real data
```

**Token expiry issues:**
```
- The server automatically refreshes tokens
- If refresh fails, it will re-authenticate automatically
- No manual intervention needed
```

**Connection timeouts:**
```
- Check internet connection
- Verify QuickBooks Online service status
- Try again - temporary network issues are handled automatically
```

## 💡 Tips for Best Results

1. **Start with sandbox** - Test with sandbox environment first
2. **Use quick access tools** - Most common reports have dedicated tools
3. **Check company info** - Each response includes company details
4. **Monitor logs** - Console shows authentication and API call progress
5. **Customize periods** - All date ranges are customizable

## 📋 Example Workflow

```python
# 1. Get overview of company finances
summary = get_company_financial_summary()

# 2. Deep dive into current performance
current_pl = get_current_month_pl()

# 3. Compare to previous period
last_month_pl = get_last_month_pl()

# 4. Check cash position
balance_sheet = generate_balance_sheet_report({})

# 5. Review outstanding receivables
ar_aging = generate_ar_aging_report({})
```

## 🆘 Support

- **QuickBooks API Docs**: [developer.intuit.com](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities)
- **FastMCP Documentation**: [fastmcp.com](https://fastmcp.com)
- **OAuth Issues**: Check redirect URI matches exactly in app settings

---

🎉 **Ready to go!** Just run `uv run qbo-mcp` and start generating reports. The server handles all the complexity automatically.
