# CityFalcon Financial News MCP Server

A Multi-agent Communications Protocol (MCP) server that provides access to CityFalcon's comprehensive financial news and data API. This server allows AI agents and other applications to retrieve real-time financial news, market data, analyst opinions, and more through standardized function calls.

## What is CityFalcon?

CityFalcon is a financial content and data discovery platform that aggregates, filters, and analyzes financial news and information from thousands of sources. The API provides access to:

- Real-time financial news
- Sentiment analysis
- Analyst price targets
- Market summaries
- Company filings
- Insider transactions
- Investor relations information

## Features

This MCP server wraps all major CityFalcon API endpoints into convenient function calls:

### News and Stories
- `get_news_by_ticker`: Get the latest news for specific stock tickers
- `get_news_by_topic`: Search for news related to financial topics
- `get_similar_stories`: Find articles similar to a specific story
- `get_stories_by_uuid`: Retrieve specific stories by their UUIDs

### Market Data
- `get_market_summary`: Get market summaries for specific assets
- `get_market_performers`: Find top gainers or losers in various asset classes

### Analysis
- `get_entity_sentiment`: Retrieve sentiment analysis for specific entities
- `extract_entities`: Extract named entities from text with financial context
- `get_analyst_price_targets`: Retrieve analyst price targets for stocks
- `get_price_targets_summary`: Get summarized price target information
- `get_price_targets_consensus`: See consensus ratings (buy/sell/hold)

### Corporate Information
- `get_company_filings`: Access regulatory filings from SEC, Companies House, etc.
- `get_insider_transactions`: Track insider buying and selling activities
- `get_investor_relations`: Access earnings calls, presentations, etc.

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

```python
# Example: Get financial news for Apple stock
result = await get_news_by_ticker("AAPL")

# Example: Search for news about inflation
result = await get_news_by_topic("inflation")

# Example: Get market summary for tech stocks
result = await get_market_summary("AAPL,MSFT,GOOG", "stocks")
```

## Tutorial for MCP Server with Claude
Or you can use the MCP server with a chatbot like Claude.
https://modelcontextprotocol.io/quickstart/server

## Integration with AI Agents

This MCP server is particularly useful for AI agents that need to access real-time financial information. When connected to language models or other AI systems, it enables them to:

1. Answer financial questions with up-to-date information
2. Provide market insights and news summaries
3. Track specific companies or financial topics
4. Monitor analyst opinions and price targets

## Acknowledgements

This project uses the [CityFalcon API](https://www.cityfalcon.com/), which requires an API key for access. Sign up at the CityFalcon website to obtain your API key.

---

**Note**: This is not an official CityFalcon product. It's an MCP server implementation that connects to their API.
