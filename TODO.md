# 📝 TODO List for CityFalcon Financial MCP Server

This document outlines the development and refactoring tasks for improving the reliability, functionality, and compatibility of the MCP server for financial data.

---

## ✅ 1. Validate API Responses Against MCP Contracts

- [X] Go through each function decorated with `@mcp.tool()`
- [X] Check the expected structure of each return (string-based, formatted content)  
- [ ] Ensure responses from all CityFalcon and DCSC endpoints are parsed correctly and safely
- [X] Confirm fallback handling is robust for malformed or empty responses  
- [ ] Update docstrings if needed to reflect exact output structure for AI agents

---

## 🔄 2. Replace Search Query Calls With Named Entity Search

- [X] Remove `get_news_by_topic()` (uses `search_query`)
- [X] Replace with dedicated functions using `identifier_type=assets` for:
  - [X] Macro entities (e.g., `inflation`, `interest rates`, `Federal Reserve System`)
  - [X] Themes or economic concepts (e.g., `recession`, `GDP`, `climate risk`)
- [-] Create a new MCP tool for each common entity:
  - e.g. `get_news_inflation()`, `get_news_fed()`, etc.
  - Use identifiers from the "assets" category, not full-text search.

> _“These are connected on our backend to various tags through our NLU layer.”_  
> Use this tagging for semantic discovery, not keyword matching.

---

## ⚠️ 3. Audit Function Purpose Clarity for the Chatbot

- [ ] Identify functions that may confuse the AI due to:
  - Misleading function names
  - Too generic parameter names
  - Ambiguous tool descriptions
- [ ] Rename functions or rewrite docstrings to better reflect intent
- [ ] Consider namespacing tools (e.g. `market_get_summary` vs. `portfolio_get_summary`)
- [ ] Add `expected_input` and `example_usage` notes in tool descriptions if needed

---

## ✨ 4. Suggested Improvements & Enhancements

### 🧪 Test Coverage
- [ ] Create test harness or unit tests for each `@mcp.tool()` function
- [ ] Use mock responses to simulate API calls (e.g. with `pytest-asyncio` and `respx`)

### 📊 Output Format Consistency
- [ ] Standardize all output sections:
  - Title/Header
  - Meta (Date, Source, Tags)
  - Body/Description
  - URLs always at end
- [ ] Consider JSON output behind a flag for agent consumption

### 🧠 Entity Extraction Extension
- [ ] Use `extract_entities()` to dynamically generate the `assets` identifiers for relevant topics
- [ ] Auto-route to `get_news_by_ticker()` or topic-specific MCP tools as needed

### 🗂️ Organize MCP Tools
- [ ] Group MCP tools by domain (e.g., `News`, `Market`, `Analysis`, `Portfolio`)
- [ ] Optionally, split files (e.g., `news_tools.py`, `dcsc_tools.py`) for maintainability

---

## 🧼 5. Cleanup and Optimization

- [ ] Remove deprecated or unused API endpoints
- [ ] Ensure timeout and error messages are standardized
- [ ] Strip out hardcoded secrets from source (`CITYFALCON_API_KEY`)
- [ ] Include `.env` and use `dotenv` for secret management

---