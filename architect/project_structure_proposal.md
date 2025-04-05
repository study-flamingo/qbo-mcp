# Project Structure

```
.
├── .clinerules
├── .gitignore
├── .python-version
├── main.py                 # Minimal entry point: CLI args, logging setup, starts server OR runs auth utility
├── pyproject.toml
├── README.md
├── requirements.txt
├── uv.lock
├── docs/
│   └── project_structure_proposal.md # This file
└── src/
    └── qbo_mcp/
        ├── __init__.py
        ├── server.py           # Defines FastMCP instance, lifespan manager (imports tools/prompts)
        ├── config.py           # Configuration loading
        ├── models/             # Package for data models
        │   ├── __init__.py
        │   ├── common.py       # Common models (e.g., QBOContext)
        │   └── tools.py        # Input/Output models specific to tools
        ├── api/                # Defines the MCP Tools and Prompts interface
        │   ├── __init__.py
        │   ├── prompts.py      # Defines @mcp.prompt functions
        │   └── tools/          # Package for tool definitions
        │       ├── __init__.py     # Imports all tool functions for easy registration
        │       ├── reports.py    # Tool definitions related to reports
        │       ├── resources.py  # Tool definitions related to resources
        │       └── search.py     # Tool definitions related to searching
        ├── services/           # Core business logic interacting with QBO SDK
        │   ├── __init__.py
        │   ├── qbo_client.py   # Handles QBO SDK client setup, connection context
        │   ├── reports.py      # Logic for generating reports
        │   ├── resources.py    # Logic for fetching resources
        │   └── search.py       # Logic for searching transactions
        └── utils/              # Utility functions
            ├── __init__.py
            ├── auth.py         # Contains OAuth flow logic (run_auth_flow) and token management
            └── formatting.py   # Helper functions for formatting results/errors
```

### Justification for Changes

1.  **Decoupled `api/` Layer:**
    *   **Addresses:** Monolithic `server.py`, Tight Coupling, Repetitive Boilerplate, Unclear Separation.
    *   **How:** Creates `api/` package. Sub-modules (`api/tools/reports.py`, etc.) define MCP tools/prompts via decorators, focusing *only* on the interface definition and orchestrating calls to `services`. `server.py` imports/registers these.
2.  **Refined `services/` Layer:**
    *   **Addresses:** Tight Coupling, SRP.
    *   **How:** `services` modules contain *only* core QBO interaction logic, returning structured data (e.g., Pydantic models from `models/`). `services/qbo_client.py` handles client lifecycle.
3.  **Dedicated `utils/` Package:**
    *   **Addresses:** OAuth Logic in `main.py`, Token Management Location, Repetitive Boilerplate.
    *   **How:** Moves `run_auth_flow` and token management to `utils/auth.py`. Moves formatting helpers to `utils/formatting.py`.
4.  **Structured `models/` Package:**
    *   **Addresses:** Clarity.
    *   **How:** Organizes Pydantic models for config, context (`common.py`), and tool I/O (`tools.py`).
5.  **Minimal `main.py`:**
    *   **Addresses:** OAuth Logic in `main.py`.
    *   **How:** `main.py` simplifies to parsing args, basic logging, and running either the auth utility or the MCP server.

### Benefits of Proposed Structure

*   **Separation of Concerns:** Clear boundaries between layers.
*   **Maintainability:** Easier to add/modify tools without impacting unrelated files.
*   **Testability:** Layers can be tested more independently.
*   **Readability:** Clearer purpose for each module/package.