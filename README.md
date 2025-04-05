# QuickBooks Online MCP Server

An MCP server that provides access to QuickBooks Online financial data and reporting capabilities through Claude Desktop. Ask questions naturally about your financial data, and Claude will help analyze and explain it.

## Features

- **Financial Data Access**
  - Get account listings (`get_accounts`)
  - Get customer information (`get_customers`)
  - Get recent invoices (`get_recent_invoices`)

- **Financial Reports**
  - Generate Profit and Loss statements (`get_profit_loss`)
  - Generate Balance Sheets (`get_balance_sheet`)
  - Get Aged Receivables reports (`get_aged_receivables`)
  - Search transaction history with filters (`search_transactions`)

- **Guided Financial Analysis**
  - Analyze cash flow (`analyze_cash_flow` prompt)
  - Perform monthly financial reviews (`monthly_review` prompt)
  - Analyze accounts receivable (`accounts_receivable_analysis` prompt)

## Prerequisites

1. Install [Claude Desktop](https://claude.ai/download)
2. Install Python 3.10 or higher
3. Set up QuickBooks Online:
   - Create a [developer account](https://developer.intuit.com/)
   - Create a new app in the Intuit Developer portal.
   - Note your **Client ID** and **Client Secret**.
   - Configure the OAuth **Redirect URI** (default used by this server is `http://localhost:8000/callback`, ensure this matches your app setup).
   - Obtain an initial **Refresh Token** through the OAuth 2.0 flow for your app (this server requires a refresh token to connect but doesn't handle the initial acquisition).
   - Know your QuickBooks **Company ID**.

## Installation

1. Install the package:
   ```bash
   # Ensure you are in the project's root directory
   pip install .
   ```

2. Configure Credentials:
   Set the following environment variables in your system or terminal session:
   - `QBO_CLIENT_ID`: Your QuickBooks App Client ID.
   - `QBO_CLIENT_SECRET`: Your QuickBooks App Client Secret.
   - `QBO_ENVIRONMENT`: `sandbox` or `production`.
   - `QBO_REDIRECT_URI`: The redirect URI configured in your app (e.g., `http://localhost:8000/callback`).
   - `QBO_COMPANY_ID`: Your QuickBooks Company ID.
   - `QBO_REFRESH_TOKEN`: The initial refresh token obtained during OAuth setup.

   *Alternatively, the server can read the refresh token from `~/.qbo-mcp/token.json` if it exists.*

## Using with Claude Desktop

1. Install the server in Claude Desktop:
   Ensure the environment variables from Step 2 are set in the terminal where you run this command.
   ```bash
   mcp install qbo-mcp
   ```
   *Alternatively, if you prefer not to set system-wide environment variables, you can create a temporary `.env` file with the variables and use the `-f` flag:*
   ```bash
   # Example temporary .env file content:
   # QBO_CLIENT_ID=YOUR_ID
   # QBO_CLIENT_SECRET=YOUR_SECRET
   # ... (other variables)

   mcp install qbo-mcp -f /path/to/your/temporary/.env
   ```

2. Start a conversation with Claude and ask questions naturally about your financial data. For example:

   - "How's our cash flow looking?"
   - "Can you review last month's financial performance?"
   - "Show me overdue receivables and suggest collection strategies"
   - "What were our total sales last quarter?"
   - "Show me all transactions with Customer X from last month"

3. Example conversation:
   ```
   You: Can you analyze our current cash flow situation?
   
   Claude: I'll help you analyze the company's cash flow situation. I'll:
   1. Review the current balance sheet to assess cash position
   2. Check aged receivables to understand collection status
   3. Identify any concerning trends
   4. Provide specific recommendations
   
   Would you like me to proceed with this analysis?
   
   You: Yes, please.
   
   [Claude will analyze the financial data and provide insights]
   ```

## Troubleshooting

Common issues and solutions:

1. **Authentication Errors**
   - Check your QBO credentials in `.env`
   - Try re-authenticating with `qbo-mcp auth`
   - Ensure your OAuth tokens are valid

2. **Connection Issues**
   - Verify your internet connection
   - Check if QBO is accessible
   - Ensure your company ID is correct

3. **Claude Desktop Integration**
   - Make sure Claude Desktop is running
   - Check if the server is properly installed
   - Verify environment variables are loaded

## Development

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Run tests:
   ```bash
   pytest
   ```

## Security

- All operations are read-only to protect financial data
- Credentials are managed through environment variables
- OAuth tokens are stored securely in the user's home directory
- Access is limited to authorized QuickBooks company accounts
- All API calls are logged for audit purposes

## License

MIT
