# CityFalcon Financial News and DCSC Portfolio Analysis MCP Server

A Multi-agent Communications Protocol (MCP) server that provides access to CityFalcon's comprehensive financial news and data API, as well as the DCSC portfolio analysis API. This server allows AI agents and other applications to retrieve real-time financial news, market data, analyst opinions, portfolio analysis, and more through standardized function calls.

## What is CityFalcon?

CityFalcon is a financial content and data discovery platform that aggregates, filters, and analyzes financial news and information from thousands of sources. The API provides access to:

- Real-time financial news
- Sentiment analysis
- Analyst price targets
- Market summaries
- Company filings
- Insider transactions
- Investor relations information

## What is DCSC?

DCSC (Digital Client Solution Center) is CityFalcon's portfolio analysis API that provides AI-powered insights into investment portfolios. DCSC offers:

- Smart portfolio analysis
- AI-based portfolio classification
- Performance and risk metrics
- Sector breakdown and analysis
- AI-classified sectors

## Features

This MCP server wraps key CityFalcon and DCSC API endpoints into convenient function calls:

### CityFalcon: News and Stories
- `get_news_by_ticker_or_topic`: Get the latest news for specific stock tickers or general financial topics
- `get_similar_stories`: Find articles similar to a specific story
- `get_stories_by_uuid`: Retrieve specific stories by their UUIDs

### CityFalcon: Analysis
- `get_entity_sentiment`: Retrieve sentiment analysis for specific entities (supports both bonds, stocks, etc.)
- `get_analyst_price_targets`: Retrieve analyst price targets for stocks
- `get_price_targets_summary`: Get summarized price target information
- `get_price_targets_consensus`: See consensus ratings (buy/sell/hold)

### CityFalcon: Corporate Information
- `get_insider_transactions`: Track insider buying and selling activities

### DCSC: Portfolio Analysis
- `get_smart_portfolio`: Get detailed information about a portfolio and its holdings
- `get_portfolio_classification`: Get AI-based classification of a portfolio's investment style
- `get_portfolio_performance`: Retrieve performance and risk metrics for a portfolio
- `get_portfolio_sectors`: Get sector breakdown for a portfolio
- `get_classified_sectors`: Get AI-classified sectors with stocks grouped by themes

## Setup

1. Clone this repository
   ```
   git clone https://github.com/delaralomen/automation_agent.git
   cd automation_agent
   ```

2. Create a virtual environment
   ```
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies from requirements.txt
   ```
   pip install -r requirements.txt
   ```

## Usage

Once the server is running, it can be accessed through any MCP client that can connect to its endpoint. Here are examples of how to use some of the functions:

### CityFalcon API Examples:
```python
# Example: Get financial news for Apple stock
result = await get_news_by_ticker_or_topic("AAPL")

# Example: Search for news about inflation
result = await get_news_by_ticker_or_topic("inflation")

# Example: Get sentiment data for stocks
result = await get_entity_sentiment("stocks", "d1")

# Example: Get analyst price targets
result = await get_analyst_price_targets("TSLA")
```

### DCSC API Examples:
```python
# Example: Get detailed portfolio analysis
result = await get_smart_portfolio("portfolio_123")

# Example: Get portfolio classification
result = await get_portfolio_classification("portfolio_123")

# Example: Get performance metrics with benchmark comparison
result = await get_portfolio_performance("portfolio_123", "benchmark_456")

# Example: Get sector breakdown
result = await get_portfolio_sectors("portfolio_123")
```

## Testing

The repository includes a comprehensive test suite in `tests.py` that tests all API endpoints. The test suite includes:

- Progress bar display of test completion
- Detailed logging of all API responses to log files
- Summary report of passed/failed tests

To run the tests:
```
python tests.py
```

Test results will be saved in the `logs` directory with timestamps for easy reference.

## Tutorial for MCP Server with Claude

You can use the MCP server with a chatbot like Claude.
https://modelcontextprotocol.io/quickstart/server

## Integration with AI Agents

This MCP server is particularly useful for AI agents that need to access real-time financial information and portfolio analysis. When connected to language models or other AI systems, it enables them to:

1. Answer financial questions with up-to-date information
2. Provide market insights and news summaries
3. Track specific companies or financial topics
4. Monitor analyst opinions and price targets
5. Analyze investment portfolios and provide insights
6. Compare portfolio performance against benchmarks
7. Identify sector exposures and investment themes

## Recent Updates

- Consolidated news functions into a single versatile `get_news_by_ticker_or_topic` function
- Enhanced error handling for API responses
- Added support for both list and dictionary response formats in entity sentiment analysis
- Created comprehensive test suite with logging capabilities
- Fixed compatibility issues with the latest CityFalcon API response formats

## Acknowledgements

This project uses the [CityFalcon API](https://www.cityfalcon.ai/) and DCSC API, which require API keys for access. Sign up at the CityFalcon website to obtain your API key.

---

**Note**: This is not an official CityFalcon product. It's an MCP server implementation that connects to their APIs.