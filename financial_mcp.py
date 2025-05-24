import asyncio  
from typing import Any, Dict, List, Optional  
import httpx  
from mcp.server.fastmcp import FastMCP  

mcp = FastMCP("financial-news")  

# API configuration  
CITYFALCON_API_KEY = ""  
CITYFALCON_API_BASE_URL = "https://api.cityfalcon.com/v0.2"  
DCSC_API_BASE_URL = "https://api.cityfalcon.com/dcsc/v0.1"

# Define headers without authorization (since we'll use query param for auth)  
HEADERS = {  
    "Content-Type": "application/json"  
}  

###################  
# API REQUEST FUNCTIONS  
###################  

# Helper function to make CityFalcon API requests  
async def make_cityfalcon_request(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:  
    url = f"{CITYFALCON_API_BASE_URL}/{endpoint}"  
    
    # Initialize params if None  
    if params is None:  
        params = {}  
    
    # Add access token to params instead of using Authorization header  
    params["access_token"] = CITYFALCON_API_KEY  
    
    async with httpx.AsyncClient() as client:  
        try:  
            response = await client.get(url, params=params, headers=HEADERS, timeout=30.0)  
            response.raise_for_status()  
            return response.json()  
        except httpx.HTTPStatusError as e:    
                print(f"❌ HTTP error for CityFalcon API endpoint {endpoint}: {e}")  
                return {"error": str(e)}  
        except Exception as e:  
            print(f"❌ Error making CityFalcon API request to {endpoint}: {e}")  
            return {"error": str(e)}  

# Helper function to make DCSC API requests  
async def make_dcsc_request(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:  
    url = f"{DCSC_API_BASE_URL}/{endpoint}"  
    
    # Initialize params if None  
    if params is None:  
        params = {}  
    
    # Add access token to params  
    params["access_token"] = CITYFALCON_API_KEY  
    
    async with httpx.AsyncClient() as client:  
        try:  
            response = await client.get(url, params=params, headers=HEADERS, timeout=30.0)  
            response.raise_for_status()  
            return response.json()  
        except httpx.HTTPStatusError as e:   
                print(f"❌ HTTP error for DCSC API endpoint {endpoint}: {e}")  
                return {"error": str(e)}  
        except Exception as e:  
            print(f"❌ Error making DCSC API request to {endpoint}: {e}")  
            return {"error": str(e)}  

###################  
# CITYFALCON FORMAT FUNCTIONS  
###################  

def format_story(story: Dict[str, Any]) -> str:  
    """Format story data in a consistent way for news results"""  
    # Extract fields with proper fallbacks  
    title = story.get("title", "No title")  
    description = story.get("description", "No description available")  
    url = story.get("url", "#")  
    lang = story.get("lang", "Unknown")  
    cityfalcon_score = story.get("cityfalconScore", "N/A")  
    
    # Source information  
    source = story.get("source", {})  
    source_name = source.get("name", "Unknown")  
    source_country = source.get("countryName", "")  
    
    # Get sentiment if available  
    sentiment = story.get("sentiment", "N/A")  
    
    # Check for paywall or registration  
    paywall = "Yes" if story.get("paywall", False) else "No"  
    registration = "Yes" if story.get("registrationRequired", False) else "No"  
    
    # Get tags if available  
    asset_tags = ", ".join(story.get("assetTags", []))  
    
    # Format the output  
    formatted = f"""  
Title: {title}  
Source: {source_name}{f" ({source_country})" if source_country else ""}  
URL: {url}  
Language: {lang}  
CityFalcon Score: {cityfalcon_score}  
Sentiment: {sentiment}  
Paywall: {paywall}  
Registration Required: {registration}  
"""  
    
    # Add asset tags if available  
    if asset_tags:  
        formatted += f"Asset Tags: {asset_tags}\n"  
    
    # Add description  
    formatted += f"Summary: {description}\n"  
    
    return formatted  

def format_price_target(target: Dict[str, Any]) -> str:  
    """Format price target data specifically for analyst price target endpoints"""  
    analyst = target.get("analyst", "Unknown")  
    firm = target.get("firm", "Unknown")  
    date = target.get("date", "Unknown")  
    previous_target = target.get("previousTarget", "N/A")  
    current_target = target.get("currentTarget", "N/A")  
    change = target.get("change", "N/A")  
    rating = target.get("rating", "N/A")  
    previous_rating = target.get("previousRating", "N/A")  
    
    return f"""  
Analyst: {analyst} ({firm})  
Date: {date}  
Current Target: {current_target}  
Previous Target: {previous_target}  
Change: {change}  
Current Rating: {rating}  
Previous Rating: {previous_rating}  
"""  

def format_filing(filing: Dict[str, Any]) -> str:  
    """Format filing data for filings endpoints"""  
    filing_id = filing.get("filing_id", "Unknown")  
    filing_type = filing.get("filing_type", "Unknown")  
    title = filing.get("title", "No title")  
    filing_date = filing.get("filing_date", "Unknown")  
    company_name = filing.get("company_name", "Unknown")  
    identifier = filing.get("identifier", "Unknown")  
    url = filing.get("url", "#")  
    
    return f"""  
Filing ID: {filing_id}  
Type: {filing_type}  
Company: {company_name} ({identifier})  
Date: {filing_date}  
Title: {title}  
URL: {url}  
"""  

def format_insider_transaction(transaction: Dict[str, Any]) -> str:  
    """Format insider transaction data"""  
    insider_name = transaction.get("insider_name", "Unknown")  
    position = transaction.get("position", "Unknown")  
    company_name = transaction.get("company_name", "Unknown")  
    transaction_type = transaction.get("transaction_type", "Unknown")  
    amount = transaction.get("amount", "N/A")  
    price = transaction.get("price", "N/A")  
    value = transaction.get("value", "N/A")  
    transaction_date = transaction.get("transaction_date", "Unknown")  
    
    return f"""  
Insider: {insider_name} ({position})  
Company: {company_name}  
Transaction: {transaction_type}  
Amount: {amount} shares  
Price: {price}  
Total Value: {value}  
Date: {transaction_date}  
"""  

def format_investor_relation(relation: Dict[str, Any]) -> str:  
    """Format investor relation data"""  
    title = relation.get("title", "No title")  
    company_name = relation.get("company_name", "Unknown")  
    relation_type = relation.get("type", "Unknown")  
    date = relation.get("date", "Unknown")  
    url = relation.get("url", "#")  
    
    return f"""  
Type: {relation_type}  
Company: {company_name}  
Date: {date}  
Title: {title}  
URL: {url}  
"""  

###################  
# DCSC FORMAT FUNCTIONS  
###################  

def format_portfolio_item(item: Dict[str, Any]) -> str:  
    """Format portfolio item data from DCSC API"""  
    ticker = item.get("ticker", "Unknown")  
    description = item.get("description", "No description available")  
    weight = item.get("weight", "N/A")  
    currency = item.get("currency", "N/A")  
    sector = item.get("sector", "N/A")  
    
    return f"""  
Ticker: {ticker}  
Description: {description}  
Weight: {weight}  
Currency: {currency}  
Sector: {sector}  
"""  

def format_portfolio_classification(classification: Dict[str, Any]) -> str:  
    """Format portfolio classification data"""  
    category = classification.get("category", "Unknown")  
    sub_category = classification.get("sub_category", "Unknown")  
    description = classification.get("description", "No description available")  
    confidence = classification.get("confidence", "N/A")  
    
    return f"""  
Category: {category}  
Sub-category: {sub_category}  
Description: {description}  
Confidence: {confidence}  
"""  

def format_performance_metric(metric: Dict[str, Any]) -> str:  
    """Format performance metric data"""  
    name = metric.get("name", "Unknown")  
    value = metric.get("value", "N/A")  
    benchmark = metric.get("benchmark", "N/A")  
    description = metric.get("description", "No description available")  
    
    return f"""  
Metric: {name}  
Value: {value}  
Benchmark: {benchmark}  
Description: {description}  
"""  

def format_sector(sector: Dict[str, Any]) -> str:  
    """Format sector data"""  
    name = sector.get("name", "Unknown")  
    weight = sector.get("weight", "N/A")  
    benchmark_weight = sector.get("benchmark_weight", "N/A")  
    active_weight = sector.get("active_weight", "N/A")  
    
    return f"""  
Sector: {name}  
Weight: {weight}  
Benchmark Weight: {benchmark_weight}  
Active Weight: {active_weight}  
"""  

def format_classified_sector(sector: Dict[str, Any]) -> str:  
    """Format classified sector data"""  
    name = sector.get("name", "Unknown")  
    description = sector.get("description", "No description available")  
    weight = sector.get("weight", "N/A")  
    stocks = sector.get("stocks", [])  
    
    formatted = f"""  
Sector: {name}  
Description: {description}  
Weight: {weight}  
Stocks:  
"""  
    
    for stock in stocks:  
        ticker = stock.get("ticker", "Unknown")  
        name = stock.get("name", "Unknown")  
        weight = stock.get("weight", "N/A")  
        formatted += f"  - {ticker} ({name}): {weight}\n"  
    
    return formatted  

###################  
# CITYFALCON API ENDPOINTS  
###################  

@mcp.tool()  
async def get_news_by_ticker_or_topic(ticker: str, limit: int = 5) -> str:  
    """
    Get the latest financial news stories related to a financial asset or topic, using CityFalcon's Stories endpoint.

    Parameters:
        ticker (str): The full ticker or asset identifier (recommended to use full-tickers for best results).
        limit (int): Maximum number of news stories to return.

    This function uses the following CityFalcon Stories endpoint parameters:
        - identifier_type: Use "assets" (preferred for companies and most assets).
        - identifiers: Comma-separated list of asset tickers (full-ticker format strongly recommended).
        - categories: Use "mp" for major publications or "all" for all sources.
        - time_filter: News from specific time window, e.g. "d1" for last 24 hours.
        - order_by: Use "latest" to return the newest first.
        - with_sentiment: If True, returns sentiment score for each story.

    Note: This endpoint works best using full tickers. For some tickers (e.g. MSFT), backend data/coverage may be limited.
    """
    params = {  
        "identifier_type": "assets",  
        "identifiers": ticker,  
        "categories": "mp",  # Major and other news publications  
        "time_filter": "d1",    # Last 24 hours  
        "order_by": "latest",  
        "with_sentiment": True,  
        "limit": limit  
    }  
    
    response = await make_cityfalcon_request("stories", params)  
    
    if "error" in response:  
        return f"Error fetching news: {response['error']}"  
    
    stories = response.get("stories", [])  
    
    if not stories:  
        return "No news found for this ticker."  
    
    formatted_stories = [format_story(story) for story in stories]  
    return "\n---\n".join(formatted_stories)

@mcp.tool()  
async def get_similar_stories(story_uuid: str, limit: int = 5) -> str:  
    """
    Get news stories that are similar to a given news story using CityFalcon's Similar Stories endpoint.

    Parameters:
        story_uuid (str): The UUID of the reference story.
        limit (int): Maximum number of similar stories to retrieve.

    This function uses the following endpoint:
        - URL: /stories/{story_uuid}/similar_stories
        - Parameters: limit

    Returns a list of up to 'limit' stories that are similar to the input story UUID.
    """
    params = {  
        "limit": limit  
    }  
    
    response = await make_cityfalcon_request(f"stories/{story_uuid}/similar_stories", params)  
    
    if "error" in response:  
        return f"Error fetching similar stories: {response['error']}"  
    
    stories = response.get("stories", [])  
    
    if not stories:  
        return "No similar stories found."  
    
    formatted_stories = [format_story(story) for story in stories]  
    return "\n---\n".join(formatted_stories)  

@mcp.tool()  
async def get_stories_by_uuid(uuids: str) -> str:  
    """
    Retrieve specific news stories by their UUID(s) via CityFalcon's Stories by UUID endpoint.

    Parameters:
        uuids (str): One or more story UUIDs, comma-separated.
        
    This endpoint is provided for special client use-cases and is not typically required for general story search.

    Uses:
        - URL: /stories/by_uuid
        - Parameters: uuids (comma-separated), with_sentiment (bool)

    Returns formatted story details for the specified UUIDs.
    """  
    params = {  
        "uuids": uuids,  
        "with_sentiment": True  
    }  
    
    response = await make_cityfalcon_request("stories/by_uuid", params)  
    
    if "error" in response:  
        return f"Error fetching stories: {response['error']}"  
    
    stories = response.get("stories", [])  
    
    if not stories:  
        return "No stories found for the provided UUIDs."  
    
    formatted_stories = [format_story(story) for story in stories]  
    return "\n---\n".join(formatted_stories)  

@mcp.tool()  
async def get_entity_sentiment(identifiers: str, period: str = "d1") -> str:  
    """
    Retrieve time-series sentiment data for one or more financial entities (companies, assets, etc.)
    using CityFalcon's Sentiment Service endpoint.

    Parameters:
        identifiers (str): The full ticker(s) or topic identifier(s).
        period (str): Time window for sentiment statistics (e.g. 'd1' for 1 day, 'w1' for 1 week).

    The endpoint provides average sentiment over the period and statistical breakdown, including
    count of stories per sentiment category.

    Uses:
        - URL: /services/sentiment
        - Parameters: identifier_type, identifiers, period, average_for_period, statistics_for_period

    Returns a summary of sentiment measures per asset/topic identifier.
    """  
    params = {  
        "identifier_type": "topic_classes",  
        "identifiers": identifiers,  
        "period": period,  
        "average_for_period": True,  
        "statistics_for_period": True  
    }  
    
    response = await make_cityfalcon_request("services/sentiment", params)  
    
    if "error" in response:  
        return f"Error fetching sentiment data: {response['error']}"  
    
    # Format the response in a readable way  
    result = f"Sentiment data for {identifiers} over period {period}:\n\n"  
    
    # Check if entities is a list (new API format) or dict (old format)  
    entities = response.get("entities", {})  
    
    if isinstance(entities, list):  
        # Handle list format  
        for entity in entities:  
            entity_id = entity.get("id", "Unknown")  
            result += f"Entity: {entity_id}\n"  
            
            # Handle average sentiment if available  
            avg = entity.get("average", {})  
            if avg:  
                result += f"  Average sentiment: {avg.get('sentiment', 'N/A')}\n"  
                result += f"  Sample size: {avg.get('sampleSize', 'N/A')}\n"  
            
            # Handle statistics if available  
            stats = entity.get("statistics", {})  
            if stats:  
                result += "  Statistics:\n"  
                for stat_period, stat_data in stats.items():  
                    result += f"    {stat_period}: {stat_data.get('sentiment', 'N/A')} (sample: {stat_data.get('sampleSize', 'N/A')})\n"  
            
            result += "\n"  
    else:  
        # Handle dictionary format (original code)  
        for entity_id, data in entities.items():  
            result += f"Entity: {entity_id}\n"  
            avg = data.get("average", {})  
            result += f"  Average sentiment: {avg.get('sentiment', 'N/A')}\n"  
            result += f"  Sample size: {avg.get('sampleSize', 'N/A')}\n"  
            
            stats = data.get("statistics", {})  
            if stats:  
                result += "  Statistics:\n"  
                for stat_period, stat_data in stats.items():  
                    result += f"    {stat_period}: {stat_data.get('sentiment', 'N/A')} (sample: {stat_data.get('sampleSize', 'N/A')})\n"  
            
            result += "\n"  
    
    return result 

@mcp.tool()  
async def get_analyst_price_targets(ticker: str) -> str:  
    """
    Retrieve analyst price targets for a given asset using CityFalcon's Analyst Price Targets endpoint.

    Parameters:
        ticker (str): Full ticker symbol of the asset (US assets only as of now).

    Uses:
        - URL: /analyst_price_targets
        - Parameters: identifier (ticker)

    Note: Endpoint is only supported for US assets, and may return empty data for others.
          If the response is empty, there is simply no data available for the asset.

    Returns formatted analyst price targets if available.
    """  
    params = {  
        "identifier": ticker  
    }  
    
    response = await make_cityfalcon_request("analyst_price_targets", params)  
    
    if "error" in response:  
        return f"Error fetching price targets: {response['error']}"  
    
    # Check if response is a list - handle directly  
    if isinstance(response, list):  
        targets = response  
    else:  
        # Original approach as fallback  
        targets = response.get("targets", [])  
    
    if not targets:  
        return f"No analyst price targets found for {ticker}."  
    
    formatted_targets = [format_price_target(target) for target in targets]  
    return f"Analyst price targets for {ticker}:\n\n" + "\n---\n".join(formatted_targets)    

@mcp.tool()  
async def get_price_targets_summary(ticker: str) -> str:  
    """
    Retrieve a summary of analyst price targets for a specific asset from CityFalcon.

    Parameters:
        ticker (str): Full ticker symbol of the asset.

    Uses:
        - URL: /analyst_price_targets/summary
        - Parameters: identifier (ticker)

    Note: Typically supported for US equities only.

    Returns key statistics such as the average, high, and low price target, and number of analysts.
    """  
    params = {  
        "identifier": ticker  
    }  
    
    response = await make_cityfalcon_request("analyst_price_targets/summary", params)  
    
    if "error" in response:  
        return f"Error fetching price targets summary: {response['error']}"  
    
    # Check if response is a list with at least one item  
    if isinstance(response, list) and response:  
        summary = response[0]  
    else:  
        # Original approach as fallback  
        summary = response.get("summary", {})  
    
    result = f"Price targets summary for {ticker}:\n\n"  
    result += f"Average target: {summary.get('average', 'N/A')}\n"  
    result += f"High target: {summary.get('high', 'N/A')}\n"  
    result += f"Low target: {summary.get('low', 'N/A')}\n"  
    result += f"Number of analysts: {summary.get('numberOfAnalysts', 'N/A')}\n"  
    
    return result    

@mcp.tool()   
async def get_price_targets_consensus(ticker: str) -> str:  
    """
    Retrieve consensus ratings of analyst price targets for a given ticker.

    Parameters:
        ticker (str): Full ticker symbol of the asset.

    Uses:
        - URL: /analyst_price_targets/consensus
        - Parameters: identifier (ticker)

    Returns an aggregate of buy, overweight, hold, underweight, and sell recommendations (if available).
    """  
    params = {  
        "identifier": ticker  
    }  
    
    response = await make_cityfalcon_request("analyst_price_targets/consensus", params)  
    
    if "error" in response:  
        return f"Error fetching price targets consensus: {response['error']}"  
    
    # Check if response is a list with at least one item  
    if isinstance(response, list) and response:  
        consensus = response[0]  
    else:  
        # Original approach as fallback  
        consensus = response.get("consensus", {})  
    
    result = f"Price targets consensus for {ticker}:\n\n"  
    result += f"Buy: {consensus.get('buy', 'N/A')}\n"  
    result += f"Overweight: {consensus.get('overweight', 'N/A')}\n"  
    result += f"Hold: {consensus.get('hold', 'N/A')}\n"  
    result += f"Underweight: {consensus.get('underweight', 'N/A')}\n"  
    result += f"Sell: {consensus.get('sell', 'N/A')}\n"  
    
    return result 

@mcp.tool()  
async def get_insider_transactions(identifiers: str, transaction_type: str = None,   
                                   page: int = 1, per_page: int = 10) -> str:  
    """Get insider transactions for specified companies."""  
    params = {  
        "identifiers": identifiers,  
        "page": page,  
        "per": per_page  
    }  
    
    if transaction_type:  
        params["transaction_type"] = transaction_type  
    
    response = await make_cityfalcon_request("insider_transactions", params)  
    
    if "error" in response:  
        return f"Error fetching insider transactions: {response['error']}"  
    
    transactions = response.get("transactions", [])  
    
    if not transactions:  
        return f"No insider transactions found for {identifiers}."  
    
    formatted_transactions = [format_insider_transaction(t) for t in transactions]  
    return f"Insider transactions for {identifiers}:\n\n" + "\n---\n".join(formatted_transactions) 

###################
# DCSC – FORMAT HELPERS
###################

def format_sector_meta(sector: Dict[str, Any]) -> str:
    """
    Convert one element returned by /v0.1/sectors into a short, readable line.

    Expected keys in *sector*:
        name (str)   – Human readable sector name, e.g. “Information Technology”
        slug (str)   – URL-safe identifier used by all other DCSC endpoints
        description  – (optional) free-text description of the sector
    """
    return f"- {sector.get('name','Unknown')}  (slug: {sector.get('slug','n/a')})" \
           + (f"\n  {sector.get('description')}" if sector.get("description") else "")


def format_sector_perf(sector: Dict[str, Any]) -> str:
    """
    Format one performance object returned by /v0.1/sectors/performance.

    Typical keys (may vary by DCSC version):
        slug, name              – sector identifiers
        price, priceChange      – latest level and Δ (abs)
        priceChangePct          – Δ in %
        period                  – time window used, e.g. “d1”, “w1”
        benchmark*, excess*     – numbers vs. benchmark (if requested)
    """
    return (
        f"{sector.get('name','Unknown')}  [{sector.get('slug')}] — {sector.get('period','n/a')}\n"
        f"  Price: {sector.get('price','n/a')}\n"
        f"  Change: {sector.get('priceChange','n/a')} "
        f"({sector.get('priceChangePct','n/a')}%)\n"
        + (
            f"  Excess vs benchmark: {sector.get('excessReturn','n/a')} "
            f"({sector.get('excessReturnPct','n/a')}%)\n"
            if 'excessReturn' in sector else ''
        )
    )

###################
# DCSC – ENDPOINT WRAPPERS (CORRECTED)
###################

@mcp.tool()
async def list_sectors() -> str:
    """
    List all sectors recognized by the DCSC data-service.

    Returns complete sector hierarchy from all levels (1, 2, 3, 4).

    Under the hood:
        GET  /v0.1/sectors
    """
    response = await make_dcsc_request("sectors")

    if "error" in response:
        return f"Error fetching sector catalogue: {response['error']}"

    # Handle different response formats
    if isinstance(response, list):
        sectors = response
    else:
        sectors = response.get("sectors", response)
    
    if not sectors:
        return "No sectors found."

    # Format the hierarchical sector data
    result = "DCSC Sector Hierarchy:\n\n"
    
    if isinstance(sectors, dict):
        for level, level_sectors in sectors.items():
            result += f"Level {level}:\n"
            for sector in level_sectors:
                name = sector.get('name', 'Unknown')
                slug = sector.get('slug', 'n/a')
                result += f"  - {name} (slug: {slug})\n"
            result += "\n"
    else:
        # If it's a flat list
        for sector in sectors:
            name = sector.get('name', 'Unknown')
            slug = sector.get('slug', 'n/a')
            level = sector.get('level', 'Unknown')
            result += f"Level {level}: {name} (slug: {slug})\n"
    
    return result


@mcp.tool()
async def get_sector_hierarchy(level: int, slug: str) -> str:
    """
    Get hierarchy for a specific sector at a given level.

    Parameters:
        level (int): Sector Level (1, 2, 3 or 4)
        slug (str): Sector slug identifier

    Endpoint:
        GET /v0.1/sectors/fetch
    """
    params = {
        "level": level,
        "slug": slug
    }

    response = await make_dcsc_request("sectors/fetch", params)

    if "error" in response:
        return f"Error fetching sector hierarchy: {response['error']}"

    result = f"Sector hierarchy for {slug} (Level {level}):\n\n"
    
    # Format the hierarchy response
    if "hierarchy" in response:
        hierarchy = response["hierarchy"]
        for item in hierarchy:
            name = item.get('name', 'Unknown')
            slug = item.get('slug', 'n/a')
            level = item.get('level', 'Unknown')
            result += f"Level {level}: {name} (slug: {slug})\n"
    else:
        result += str(response)
    
    return result


@mcp.tool()
async def get_smart_portfolio(
    level: int,
    slugs: str,
    max_securities: int = 10,
    min_relevance: int = 10,
    min_confidence: int = 20,
    company_type: str = "public",
    countries: str = "all",
    allocation_type: str = "relevance"
) -> str:
    """
    Get relevant companies for given sector(s).

    Parameters:
        level (int): Sector Level (1, 2, 3 or 4)
        slugs (str): Comma separated sector slugs (max 20)
        max_securities (int): Number of companies to return (1-200, default: 10)
        min_relevance (int): Minimum relevance (1-100, default: 10)
        min_confidence (int): Minimum confidence (0-100, default: 20)
        company_type (str): "public", "private" or "both" (default: "public")
        countries (str): Comma separated country codes or "all" (default: "all")
        allocation_type (str): "relevance" or "equal" (default: "relevance")

    Endpoint:
        GET /v0.1/smart_portfolio
    """
    params = {
        "level": level,
        "slugs": slugs,
        "max_securities": max_securities,
        "min_relevance": min_relevance,
        "min_confidence": min_confidence,
        "company_type": company_type,
        "countries": countries,
        "allocation_type": allocation_type
    }

    response = await make_dcsc_request("smart_portfolio", params)

    if "error" in response:
        return f"Error fetching smart portfolio: {response['error']}"

    result = f"Smart Portfolio for sectors {slugs} (Level {level}):\n\n"
    
    # Format portfolio companies
    if "portfolio" in response:
        portfolio = response["portfolio"]
        for company in portfolio:
            name = company.get('name', 'Unknown')
            ticker = company.get('ticker', 'N/A')
            allocation = company.get('allocation', 'N/A')
            relevance = company.get('relevance', 'N/A')
            confidence = company.get('confidence', 'N/A')
            result += f"• {name} ({ticker})\n"
            result += f"  Allocation: {allocation}%\n"
            result += f"  Relevance: {relevance}\n"
            result += f"  Confidence: {confidence}\n\n"
    else:
        result += str(response)
    
    return result


@mcp.tool()
async def get_portfolio_classification(
    identifiers: str,
    identifier_type: str = "slug",
    allocation: str = None,
    min_relevance: int = 10,
    min_confidence: int = 20,
    level: int = None,
    show_missing_sectors: bool = True,
    missing_sectors_limit: int = 10
) -> str:
    """
    Get relevant sectors for given companies.

    Parameters:
        identifiers (str): Comma separated company identifiers (max 200)
        identifier_type (str): "slug", "name", "ticker", "full_ticker", or "legal_id" (default: "slug")
        allocation (str): Comma separated percentage values for corresponding identifiers
        min_relevance (int): Minimum relevance (1-100, default: 10)
        min_confidence (int): Minimum confidence (0-100, default: 20)
        level (int): Return only sectors of this level (1, 2, 3 or 4)
        show_missing_sectors (bool): Show missing sectors in summary (default: True)
        missing_sectors_limit (int): Number of missing sectors per level (default: 10)

    Endpoint:
        GET /v0.1/portfolio_classification
    """
    params = {
        "identifiers": identifiers,
        "identifier_type": identifier_type,
        "min_relevance": min_relevance,
        "min_confidence": min_confidence,
        "show_missing_sectors": show_missing_sectors,
        "missing_sectors_limit": missing_sectors_limit
    }
    
    if allocation:
        params["allocation"] = allocation
    if level:
        params["level"] = level

    response = await make_dcsc_request("portfolio_classification", params)

    if "error" in response:
        return f"Error fetching portfolio classification: {response['error']}"

    result = f"Portfolio Classification for {identifiers}:\n\n"
    
    # Format classification results
    if "classification" in response:
        classification = response["classification"]
        for sector in classification:
            name = sector.get('name', 'Unknown')
            slug = sector.get('slug', 'N/A')
            level = sector.get('level', 'N/A')
            allocation = sector.get('allocation', 'N/A')
            relevance = sector.get('relevance', 'N/A')
            confidence = sector.get('confidence', 'N/A')
            result += f"Level {level}: {name} (slug: {slug})\n"
            result += f"  Allocation: {allocation}%\n"
            result += f"  Relevance: {relevance}\n"
            result += f"  Confidence: {confidence}\n\n"
    else:
        result += str(response)
    
    return result


@mcp.tool()
async def get_portfolio_performance_risk(
    identifiers: str,
    identifier_type: str = "slug",
    allocation: str = None,
    period: str = "1y"
) -> str:
    """
    Calculate performance and risk of a portfolio.

    Parameters:
        identifiers (str): Comma separated company identifiers (max 200)
        identifier_type (str): "slug", "name", "ticker", or "full_ticker" (default: "slug")
        allocation (str): Comma separated percentage values for corresponding identifiers
        period (str): Time period for calculation (default: "1y")

    Endpoint:
        GET /v0.1/portfolio_perf_risk
    """
    params = {
        "identifiers": identifiers,
        "identifier_type": identifier_type,
        "period": period
    }
    
    if allocation:
        params["allocation"] = allocation

    response = await make_dcsc_request("portfolio_perf_risk", params)

    if "error" in response:
        return f"Error calculating portfolio performance: {response['error']}"

    result = f"Portfolio Performance & Risk Analysis ({period}):\n\n"
    
    # Format performance metrics
    if "performance" in response:
        perf = response["performance"]
        result += f"Total Return: {perf.get('total_return', 'N/A')}%\n"
        result += f"Annualized Return: {perf.get('annualized_return', 'N/A')}%\n"
        result += f"Volatility: {perf.get('volatility', 'N/A')}%\n"
        result += f"Sharpe Ratio: {perf.get('sharpe_ratio', 'N/A')}\n"
        result += f"Max Drawdown: {perf.get('max_drawdown', 'N/A')}%\n"
    
    if "risk" in response:
        risk = response["risk"]
        result += f"\nRisk Metrics:\n"
        result += f"Value at Risk (95%): {risk.get('var_95', 'N/A')}%\n"
        result += f"Expected Shortfall: {risk.get('expected_shortfall', 'N/A')}%\n"
    
    if not ("performance" in response or "risk" in response):
        result += str(response)
    
    return result


@mcp.tool()
async def get_classified_sectors_mapping(
    classification_name: str,
    sector_name: str = None,
    sector_number: str = None
) -> str:
    """
    Get corresponding DCSC sector(s) for other classification systems.

    Parameters:
        classification_name (str): Classification system name (e.g., "NAICS")
        sector_name (str): Name of sector in original system (optional)
        sector_number (str): Comma-separated sector numbers (max 10, optional)

    Note: Either sector_name or sector_number must be provided.

    Endpoint:
        GET /v0.1/classified_sectors/mappings
    """
    params = {
        "classification_name": classification_name
    }
    
    if sector_name:
        params["sector_name"] = sector_name
    elif sector_number:
        params["sector_number"] = sector_number
    else:
        return "Error: Either sector_name or sector_number must be provided"

    response = await make_dcsc_request("classified_sectors/mappings", params)

    if "error" in response:
        return f"Error fetching sector mappings: {response['error']}"

    result = f"DCSC Sector Mappings for {classification_name}:\n\n"
    
    if "mappings" in response:
        mappings = response["mappings"]
        for mapping in mappings:
            original_name = mapping.get('original_sector_name', 'N/A')
            original_number = mapping.get('original_sector_number', 'N/A')
            dcsc_sectors = mapping.get('dcsc_sectors', [])
            
            result += f"Original: {original_name} ({original_number})\n"
            result += "DCSC Sectors:\n"
            for dcsc_sector in dcsc_sectors:
                name = dcsc_sector.get('name', 'Unknown')
                slug = dcsc_sector.get('slug', 'N/A')
                level = dcsc_sector.get('level', 'N/A')
                confidence = dcsc_sector.get('confidence', 'N/A')
                result += f"  - Level {level}: {name} (slug: {slug}) [Confidence: {confidence}]\n"
            result += "\n"
    else:
        result += str(response)
    
    return result


############
#HELP FUNC##
############

@mcp.tool()
async def list_available_capabilities() -> str:
    """
    List all available MCP tools and their capabilities for financial data analysis.
    
    This tool provides a comprehensive overview of what functionality is available
    through this MCP server, including both CityFalcon and DCSC API endpoints.
    
    Returns:
        str: A formatted description of all available tools and their capabilities.
    """
    
    capabilities = """
🔧 AVAILABLE MCP TOOLS & CAPABILITIES
=====================================

📰 CITYFALCON NEWS & SENTIMENT TOOLS
------------------------------------

1. get_news_by_ticker_or_topic(ticker, limit=5)
   • Get latest financial news stories for any asset or topic
   • Uses full ticker symbols (recommended format)
   • Returns formatted news with sentiment, source, paywall info
   • Time filter: last 24 hours from major publications

2. get_similar_stories(story_uuid, limit=5)
   • Find news stories similar to a given reference story
   • Requires a story UUID from previous news searches
   • Useful for discovering related coverage

3. get_stories_by_uuid(uuids)
   • Retrieve specific news stories by their UUID(s)
   • Input: comma-separated UUIDs
   • For special use cases when you have specific story IDs

4. get_entity_sentiment(identifiers, period="d1")
   • Get time-series sentiment analysis for financial entities
   • Periods: d1 (1 day), w1 (1 week), etc.
   • Returns average sentiment and statistical breakdown
   • Shows story count per sentiment category

📊 ANALYST & PRICE TARGET TOOLS (US Assets)
-------------------------------------------

5. get_analyst_price_targets(ticker)
   • Get detailed analyst price targets for US stocks
   • Shows individual analyst recommendations with firm names
   • Includes current/previous targets and rating changes

6. get_price_targets_summary(ticker)
   • Get statistical summary of price targets
   • Returns average, high, low targets + analyst count
   • Quick overview of consensus expectations

7. get_price_targets_consensus(ticker)
   • Get breakdown of analyst ratings consensus
   • Shows buy/overweight/hold/underweight/sell counts
   • Useful for understanding overall analyst sentiment

👥 INSIDER TRADING TOOLS
------------------------

8. get_insider_transactions(identifiers, transaction_type=None, page=1, per_page=10)
   • Track insider buying/selling activity
   • Filter by transaction type if needed
   • Shows insider name, position, transaction details
   • Pagination support for large datasets

🏭 DCSC SECTOR ANALYSIS TOOLS
-----------------------------

9. list_sectors()
   • Get complete catalog of available sectors
   • Returns sector names and slugs for use in other DCSC tools
   • Essential first step for sector analysis

10. get_sector_performance(slugs, period="d1", benchmark=None)
    • Get performance data for one or multiple sectors
    • Periods: d1, w1, m1, ytd
    • Optional benchmark comparison
    • Shows price changes (absolute and percentage)

11. get_sector_history(slug, start, end, interval="d1")
    • Download historical sector performance data
    • Date range: ISO format (YYYY-MM-DD)
    • Intervals: d1 (daily), w1 (weekly), m1 (monthly)
    • Returns time series data in table format

💡 USAGE TIPS
-------------
• Use full ticker symbols (e.g., "AAPL" not "Apple") for best results
• Start with list_sectors() to see available sector slugs for DCSC tools
• Price target tools work primarily with US equities
• News tools support both individual tickers and broader topics
• Sentiment analysis helps gauge market mood around specific assets
• Combine tools for comprehensive analysis (news + sentiment + analyst targets)

🔑 DATA SOURCES
---------------
• CityFalcon API: Financial news, sentiment, analyst data, insider transactions
• DCSC API: Sector performance, historical data, sector classifications
"""
    
    return capabilities

# Start the MCP server  
if __name__ == "__main__":  
    print("MCP running with CityFalcon and DCSC APIs")  
    # Initialize and run the server  
    mcp.run(transport='stdio')