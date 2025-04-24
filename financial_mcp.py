import asyncio
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("financial-news")

# Constants
API_KEY = ""
NEWS_API_URL = "https://api.marketaux.com/v1/news/all"

# Fetch news function
async def fetch_financial_news(ticker: str) -> list[dict[str, Any]] | None:
    params = {
        "symbols": ticker.upper(),
        "filter_entities": True,
        "language": "en",
        "api_token": API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(NEWS_API_URL, params=params, timeout=30.0)
            response.raise_for_status()
            json_data = response.json()
            return json_data.get("data", [])
        except Exception as e:
            print(f"❌ Error fetching news: {e}")
            return None

# Tool definition
@mcp.tool()
async def get_financial_news(ticker: str) -> str:
    """Get latest financial news for a stock ticker."""
    news_items = await fetch_financial_news(ticker)

    if not news_items:
        return "Unable to fetch financial news."

    def format_item(item):
        entity = item.get("entities", [{}])[0]
        symbol = entity.get("symbol", "N/A")
        sentiment = entity.get("sentiment_score", "N/A")

        return f"""
Title: {item.get("title", "No title")}
Published: {item.get("published_at", "Unknown")}
Source: {item.get("source", "Unknown")}
Symbol: {symbol}
Sentiment: {sentiment}
Summary: {item.get("description", "No summary available")}
URL: {item.get("url", "#")}
"""

    formatted = [format_item(i) for i in news_items if isinstance(i, dict)]
    return "\n---\n".join(formatted[:5])  # Limit to top 5


# Only test if run as a script, NOT from MCP
# if __name__ == "__main__":
#     # You can directly call the tool function here
#     result = asyncio.run(get_financial_news("AAPL"))
#     print("📰 Financial News Output:\n", result)


if __name__ == "__main__":
    print("MCP running")
    # Initialize and run the server
    mcp.run(transport='stdio')