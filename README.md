# QuickBooks Online MCP Server

An MCP server that provides access to QuickBooks Online financial data and reporting capabilities through Claude Desktop. Ask questions naturally about your financial data, and Claude will help analyze and explain it.

## Features

- **Financial Data Access**
  - Account listings and balances
  - Customer information
  - Recent invoices and transactions
  
- **Financial Reports**
  - Profit and Loss statements
  - Balance Sheets
  - Aged Receivables
  - Transaction history

- **Financial Analysis**
  - Cash flow analysis
  - Monthly performance reviews
  - Accounts receivable management
  - Custom date range analysis

## Prerequisites

1. Install [Claude Desktop](https://claude.ai/download)
2. Install Python 3.10 or higher
3. Set up QuickBooks Online:
   - Create a [developer account](https://developer.intuit.com/)
   - Create a new app in the Intuit Developer portal
   - Get your client ID and secret
   - Configure OAuth redirect URI as `http://localhost:8000/callback`
   - Enable the following scopes:
     - Accounting
     - OpenID
     - Email

## Installation

1. Install the package:
   ```bash
   pip install .
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your QBO credentials
   ```

3. Authenticate with QuickBooks Online:
   ```bash
   # This will open your browser for QBO authentication
   qbo-mcp auth
   ```

## Using with Claude Desktop

1. Install the server in Claude Desktop:
   ```bash
   mcp install qbo-mcp -f .env
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
