# Quickbooks Online MCP Server Design & Planning

This is an MCP server that allows LLMs to interact with the [Quickbooks Online API](https://developer.intuit.com/app/developer/qbo/docs/get-started).

## Project Structure

root/
    main.py  # Helper script to start server during dev from root
    .gitignore
    pyproject.toml
    README.md
    requirements.txt
    uv.lock
    .llms/
        architect/
            .clinerules  # Deprecated LLM instructions
            project_structure_proposal.md  # This document
        docs/
            FastMCP_docs.md  # 
    .venv/ ...
