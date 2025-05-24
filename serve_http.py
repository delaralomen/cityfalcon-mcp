from fastapi import FastAPI
from financial_mcp import mcp
from financial_mcp import (
    get_news_by_ticker_or_topic,
    get_entity_sentiment,
    get_analyst_price_targets,
    get_price_targets_summary,
    get_price_targets_consensus,
    get_insider_transactions,
)

app = FastAPI(title="Financial MCP API")

@app.get("/tools/get_news_by_ticker_or_topic")
async def http_news(ticker: str, limit: int = 3):
    return await get_news_by_ticker_or_topic(ticker, limit)

@app.get("/tools/get_entity_sentiment")
async def http_sentiment(identifiers: str, period: str = "d1"):
    return await get_entity_sentiment(identifiers, period)

@app.get("/tools/get_analyst_price_targets")
async def http_targets(ticker: str):
    return await get_analyst_price_targets(ticker)

@app.get("/tools/get_price_targets_summary")
async def http_summary(ticker: str):
    return await get_price_targets_summary(ticker)

@app.get("/tools/get_price_targets_consensus")
async def http_consensus(ticker: str):
    return await get_price_targets_consensus(ticker)

@app.get("/tools/get_insider_transactions")
async def http_insiders(identifiers: str, transaction_type: str = None, per_page: int = 3):
    return await get_insider_transactions(identifiers, transaction_type, per_page=per_page)

# 🔧 Attach app to MCP
mcp.app = app

if __name__ == "__main__":
    print("🚀 Serving FastAPI + SSE MCP on default port")
    mcp.run(transport="sse")  
