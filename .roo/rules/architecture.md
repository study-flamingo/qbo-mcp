# QuickBooks Online MCP Server - Architecture Documentation

## Overview

The QuickBooks Online MCP Server is a Model Context Protocol (MCP) server that provides seamless integration with QuickBooks Online for financial reporting and data access. Built with FastMCP 2.9, it offers automatic OAuth authentication and comprehensive financial reporting tools.

## Architecture Principles

### **Separation of Concerns**

Clear boundaries between authentication (auth), business logic (reports), API interface (server), configuration (config), and data models (models).

### **Automatic Authentication**

Zero-touch OAuth flow that handles authentication automatically without exposing auth complexity to the LLM or end users.

### **Simplicity Over Complexity**

Direct, flat module structure that's easy to understand and maintain. Adding new reports involves minimal file changes.

### **Leveraging Official Packages**

Uses `intuit-oauth` package for OAuth operations and `python-quickbooks` for QuickBooks API interactions rather than building custom implementations.

### **LLM-Friendly Interface**

Tools are designed to be self-contained and require minimal context, with automatic error handling and clear response formats.

## Current Project Structure

```
qbo-mcp/
├── .env.example                # Environment configuration template
├── .gitignore                  # Git ignore rules
├── .python-version             # Python version specification
├── pyproject.toml              # Project dependencies and configuration
├── requirements.txt            # Legacy dependency specification
├── uv.lock                     # UV lock file for reproducible builds
├── README.md                   # Project documentation
├── __main__.py                 # CLI entry point
├── .roo/                       # Development tooling
│   └── rules/
│       └── architecture.md     # This file
└── src/qbo_mcp/               # Main package
    ├── __init__.py             # Package initialization and main() function
    ├── __main__.py             # Module execution entry point
    ├── server.py               # FastMCP server instance and tool registration
    ├── config.py               # Configuration management and validation
    ├── auth.py                 # OAuth authentication using intuit-oauth
    ├── reports.py              # QuickBooks report generation logic
    ├── models.py               # Pydantic models for tool inputs
    ├── resources.py            # (Reserved for future resource management)
    └── tools.py                # MCP tool definitions and helper functions
```

## Core Components

### **1. tools.py** - MCP Tool Definitions

- **Defines all MCP tools** with `@mcp.tool()` decorator
- **Contains helper functions** for report generation and data processing
- **Integrates with authentication** and report generation logic

**Key Functions:**

- `generate_profit_loss_report()` - P&L reports with custom periods
- `generate_balance_sheet_report()` - Balance sheet as of any date
- `generate_cash_flow_report()` - Cash flow statements
- `generate_ar_aging_report()` - A/R aging analysis
- `generate_ap_aging_report()` - A/P aging analysis
- `generate_sales_by_customer_report()` - Sales by customer report
- `generate_expenses_by_vendor_report()` - Expenses by vendor report
- `get_current_month_pl()` - Quick access current month P&L
- `get_current_quarter_pl()` - Quick access current quarter P&L
- `get_current_year_pl()` - Quick access current year P&L
- `get_last_month_pl()` - Quick access last month P&L
- `get_company_financial_summary()` - Comprehensive overview

### **2. server.py** - FastMCP Server Instance

- **Initializes and runs** the FastMCP server
- **Imports and registers** tools defined in `tools.py`
- **Configures logging** and performs startup checks

### **3. auth.py** - Authentication Layer

- **QBOAuthManager** class managing OAuth state
- **Automatic browser-based** OAuth flow
- **Local callback server** for OAuth redirects
- **Token persistence** and automatic refresh
- **Leverages intuit-oauth package** for core OAuth operations

**Key Features:**

- Uses `AuthClient` from `intuit-oauth` package
- Automatic token refresh with `auth_client.refresh()`
- Proper error handling with `AuthClientError`
- State persistence to disk with JSON storage
- Browser automation for seamless UX

### **4. reports.py** - Business Logic Layer

- **QBOReportsGenerator** class for report creation
- **Report processing** and data transformation
- **Period utilities** for common date ranges
- **Integration** with python-quickbooks package

**Supported Reports:**

- Profit & Loss Statement
- Balance Sheet
- Cash Flow Statement
- Accounts Receivable Aging
- Accounts Payable Aging
- Sales by Customer
- Expenses by Vendor

### **5. config.py** - Configuration Management

- **QBOConfig** class with environment variable loading
- **Configuration validation** and error reporting
- **Environment support** (sandbox/production)
- **Default values** and validation rules

### **6. models.py** - Data Models

- **Pydantic models** for tool input validation
- **Type safety** and automatic documentation
- **Reusable components** for common data structures
- **Explicitly exports** models via `__all__` for clear API

## Data Flow

```
LLM Request → FastMCP Tool → Auth Check → QB API → Report Processing → Response
     ↓              ↓            ↓           ↓           ↓             ↓
   User calls    server.py   auth.py   reports.py   python-qb   Formatted JSON
  report tool   validates   ensures   generates    fetches      back to LLM
                  input      auth      report       data
```

## Authentication Flow

```
1. Tool Called → Check auth_client.access_token
                      ↓
2. If missing → Start OAuth Flow:
   - Start local callback server (localhost:8080)
   - Generate auth URL with auth_client.get_authorization_url()
   - Open browser automatically
   - Wait for user authorization
   - Handle callback with auth_client.get_bearer_token()
   - Save tokens to disk
                      ↓
3. If expired → Refresh with auth_client.refresh()
                      ↓
4. Create QuickBooks client with valid tokens
                      ↓
5. Generate requested report
```

## Technology Stack

### **Core Dependencies**

- **FastMCP 2.9** - MCP server framework
- **intuit-oauth 1.2.6+** - Official Intuit OAuth client
- **python-quickbooks 0.9.12+** - QuickBooks API wrapper
- **python-dotenv** - Environment variable management
- **pydantic** - Data validation and models

### **Development Tools**

- **Python 3.12+** - Modern Python features
- **UV** - Fast Python package manager
- **Ruff** - Fast Python linter and formatter

## Design Decisions

### **Why Flat Module Structure?**

- **Simplicity** - Easy to understand and navigate
- **Direct imports** - Clear dependency relationships
- **Minimal boilerplate** - Less ceremony, more functionality
- **Easy testing** - Each module can be tested independently

### **Why Automatic Authentication?**

- **Better UX** - No manual OAuth steps for users
- **LLM-friendly** - No auth tokens exposed to LLM
- **Robust** - Handles token refresh automatically
- **Secure** - Tokens stored locally, not in conversation

### **Why FastMCP?**

- **Modern framework** - Built for MCP specification
- **Type safety** - Pydantic integration out of the box
- **Developer friendly** - Decorators and automatic validation
- **Performance** - Async-first design

## Extension Points

### **Adding New Reports**

1. Add method to `QBOReportsGenerator` in `reports.py`
2. Add Pydantic model to `models.py` (if needed)
3. Add tool function to `tools.py` with `@mcp.tool()` decorator and import it in `server.py`
4. Update README with new tool documentation

### **Adding New Data Sources**

1. Create new service module (e.g., `transactions.py`)
2. Add authentication integration
3. Create corresponding tools in `tools.py` and import them in `server.py`
4. Add models for new data types

### **Custom Authentication**

- Extend `QBOAuthManager` class
- Override `ensure_authenticated()` method
- Maintain compatibility with existing interface

## Testing Strategy

### **Unit Testing**

- Test each module independently
- Mock QuickBooks API responses
- Test configuration validation
- Test report processing logic

### **Integration Testing**

- Test OAuth flow end-to-end
- Test report generation with real sandbox data
- Test error handling scenarios

### **Development Testing**

- Use QuickBooks sandbox environment
- Test with sample companies
- Validate all report types

## Security Considerations

- **Local token storage** - Tokens stored on local filesystem
- **Environment variables** - Sensitive config via .env files
- **OAuth 2.0 flow** - Industry standard authentication
- **No token exposure** - LLM never sees authentication details
- **Sandbox testing** - Safe development environment

## Performance Considerations

- **Lazy authentication** - Only authenticate when needed
- **Token caching** - Reuse valid tokens across requests
- **Async operations** - Non-blocking OAuth flows
- **Efficient imports** - Fast startup times

## Deployment

### **Development**

```bash
# Setup
cp .env.example .env
# Edit .env with QB credentials
uv sync

# Run
uv run qbo-mcp
```

### **Production Considerations**

- Secure credential storage
- Log management and monitoring
- Error reporting and alerting
- Token rotation policies

## Maintenance

### **Regular Updates**

- Keep dependencies current
- Monitor QuickBooks API changes
- Update documentation
- Review security practices

### **Monitoring**

- Authentication success rates
- API call performance
- Error frequency and types
- User experience metrics

---

## Commit Message Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - New features
- `fix:` - Bug fixes  
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

**Examples:**

- `feat(reports): add sales by customer report`
- `fix(auth): handle token refresh edge case`
- `docs(readme): update installation instructions`
