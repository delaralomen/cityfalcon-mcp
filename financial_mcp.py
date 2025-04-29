import asyncio  
from typing import Any, Dict, List, Optional  
import httpx  
from mcp.server.fastmcp import FastMCP  

mcp = FastMCP("financial-news")  

# API configuration  
CITYFALCON_API_KEY = "9f3a1a3b0b210e3d1d8eac863eb06cf11fee97f9347c46a6894cffd17ab3b698"  
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
async def get_news_by_ticker(ticker: str, limit: int = 5) -> str:  
    """Get latest financial news for a stock ticker."""  
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
async def get_news_by_topic(topic: str, limit: int = 5) -> str:  
    """Get latest financial news related to a general topic (e.g., 'inflation', 'interest rates')."""  
    params = {  
        "search_query": topic,  
        "categories": "mp",  
        "time_filter": "d1",  
        "order_by": "latest",  
        "with_sentiment": True,  
        "limit": limit  
    }  
    
    response = await make_cityfalcon_request("stories", params)  
    
    if "error" in response:  
        return f"Error fetching topic news: {response['error']}"  
    
    stories = response.get("stories", [])  
    
    if not stories:  
        return "No news found for this topic."  
    
    formatted_stories = [format_story(story) for story in stories]  
    return "\n---\n".join(formatted_stories)  

@mcp.tool()  
async def get_similar_stories(story_uuid: str, limit: int = 5) -> str:  
    """Get similar news articles to a specific story by UUID."""  
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
    """Get specific stories by their UUIDs (comma-separated)."""  
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
    """Get sentiment data for entities (stocks, topics, etc.)"""  
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
    
    entities = response.get("entities", {})  
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
async def extract_entities(text: str, language: str = "EN") -> str:  
    """Extract entities from provided text."""  
    params = {  
        "text": text,  
        "language": language  
    }  
    
    response = await make_cityfalcon_request("services/entity_extraction", params)  
    
    if "error" in response:  
        return f"Error extracting entities: {response['error']}"  
    
    entities = response.get("entities", [])  
    
    if not entities:  
        return "No entities found in the provided text."  
    
    result = "Extracted entities:\n\n"  
    
    for entity in entities:  
        name = entity.get("name", "Unknown")  
        entity_type = entity.get("type", "Unknown")  
        score = entity.get("score", "N/A")  
        result += f"- {name} (Type: {entity_type}, Score: {score})\n"  
    
    return result  

@mcp.tool()  
async def get_analyst_price_targets(ticker: str) -> str:  
    """Get analyst price targets for a specific ticker."""  
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
    """Get a summary of analyst price targets for a specific ticker."""  
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
    """Get consensus of analyst price targets for a specific ticker."""  
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
async def get_company_filings(source: str, identifiers: str, identifier_type: str = "full_ticker",   
                              filing_types: str = None, page: int = 1, per_page: int = 10) -> str:  
    """Get company filings from various sources (e.g., SEC, Companies House)."""  
    params = {  
        "source": source,  
        "identifier_type": identifier_type,  
        "identifiers": identifiers,  
        "page": page,  
        "per": per_page  
    }  
    
    if filing_types:  
        params["filing_types"] = filing_types  
    
    response = await make_cityfalcon_request("filings", params)  
    
    if "error" in response:  
        return f"Error fetching filings: {response['error']}"  
    
    filings = response.get("filings", [])  
    
    if not filings:  
        return f"No filings found for {identifiers} from {source}."  
    
    formatted_filings = [format_filing(filing) for filing in filings]  
    return f"Filings for {identifiers} from {source}:\n\n" + "\n---\n".join(formatted_filings)  

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

@mcp.tool()  
async def get_investor_relations(identifiers: str, type_filter: str = None,  
                                page: int = 1, per_page: int = 10) -> str:  
    """Get investor relations data for specified companies."""  
    params = {  
        "identifiers": identifiers,  
        "page": page,  
        "per": per_page  
    }  
    
    if type_filter:  
        params["type"] = type_filter  
    
    response = await make_cityfalcon_request("investor_relations", params)  
    
    if "error" in response:  
        return f"Error fetching investor relations data: {response['error']}"  
    
    relations = response.get("relations", [])  
    
    if not relations:  
        return f"No investor relations data found for {identifiers}."  
    
    formatted_relations = [format_investor_relation(r) for r in relations]  
    return f"Investor relations for {identifiers}:\n\n" + "\n---\n".join(formatted_relations)  

@mcp.tool()  
async def get_market_summary(identifiers: str, asset_class: str = "stocks") -> str:  
    """Get market summary for specified identifiers."""  
    params = {  
        "identifiers": identifiers,  
        "asset_class": asset_class  
    }  
    
    response = await make_cityfalcon_request("market_summary", params)  
    
    if "error" in response:  
        return f"Error fetching market summary: {response['error']}"  
    
    summary = response.get("summary", {})  
    
    result = f"Market summary for {identifiers} ({asset_class}):\n\n"  
    
    for item_id, data in summary.items():  
        result += f"Asset: {item_id}\n"  
        result += f"  Name: {data.get('name', 'N/A')}\n"  
        result += f"  Price: {data.get('price', 'N/A')}\n"  
        result += f"  Change: {data.get('change', 'N/A')}\n"  
        result += f"  Change (%): {data.get('change_percent', 'N/A')}%\n"  
        result += f"  Market Cap: {data.get('market_cap', 'N/A')}\n"  
        result += f"  Volume: {data.get('volume', 'N/A')}\n\n"  
    
    return result  

@mcp.tool()  
async def get_market_performers(asset_class: str = "stocks", period: str = "d1",   
                               direction: str = "gainers", page: int = 1, per_page: int = 5) -> str:  
    """Get top market performers (gainers or losers)."""  
    params = {  
        "asset_class": asset_class,  
        "period": period,  
        "direction": direction,  
        "page": page,  
        "per": per_page  
    }  
    
    response = await make_cityfalcon_request("market_summary/performers", params)  
    
    if "error" in response:  
        return f"Error fetching market performers: {response['error']}"  
    
    performers = response.get("performers", [])  
    
    if not performers:  
        return f"No {direction} found for {asset_class} over {period}."  
    
    result = f"Top {direction} for {asset_class} over {period}:\n\n"  
    
    for p in performers:  
        result += f"- {p.get('name', 'Unknown')} ({p.get('ticker', 'Unknown')})\n"  
        result += f"  Price: {p.get('price', 'N/A')}\n"  
        result += f"  Change: {p.get('change', 'N/A')}\n"  
        result += f"  Change (%): {p.get('change_percent', 'N/A')}%\n"  
        result += f"  Market Cap: {p.get('market_cap', 'N/A')}\n\n"  
    
    return result  

###################  
# DCSC API ENDPOINTS  
###################  

@mcp.tool()  
async def get_smart_portfolio(portfolio_id: str) -> str:  
    """Get detailed information about a smart portfolio."""  
    params = {  
        "portfolio_id": portfolio_id  
    }  
    
    response = await make_dcsc_request("smart_portfolio", params)  
    
    if "error" in response:  
        return f"Error fetching smart portfolio: {response['error']}"  
    
    portfolio = response.get("portfolio", {})  
    
    result = f"Smart Portfolio: {portfolio.get('name', 'Unnamed Portfolio')}\n\n"  
    result += f"Description: {portfolio.get('description', 'No description available')}\n"  
    result += f"Currency: {portfolio.get('currency', 'N/A')}\n\n"  
    
    holdings = portfolio.get("holdings", [])  
    
    if not holdings:  
        result += "No holdings found in this portfolio."  
        return result  
    
    result += "Holdings:\n\n"  
    
    formatted_holdings = [format_portfolio_item(holding) for holding in holdings]  
    return result + "\n---\n".join(formatted_holdings)  

@mcp.tool()  
async def get_portfolio_classification(portfolio_id: str) -> str:  
    """Get classification data for a portfolio."""  
    params = {  
        "portfolio_id": portfolio_id  
    }  
    
    response = await make_dcsc_request("portfolio_classification", params)  
    
    if "error" in response:  
        return f"Error fetching portfolio classification: {response['error']}"  
    
    classifications = response.get("classifications", [])  
    
    if not classifications:  
        return f"No classification data found for portfolio {portfolio_id}."  
    
    result = f"Portfolio Classification for ID {portfolio_id}:\n\n"  
    
    formatted_classifications = [format_portfolio_classification(cls) for cls in classifications]  
    return result + "\n---\n".join(formatted_classifications)  

@mcp.tool()  
async def get_portfolio_performance(portfolio_id: str, benchmark_id: str = None) -> str:  
    """Get performance and risk metrics for a portfolio."""  
    params = {  
        "portfolio_id": portfolio_id  
    }  
    
    if benchmark_id:  
        params["benchmark_id"] = benchmark_id  
    
    response = await make_dcsc_request("portfolio_performance", params)  
    
    if "error" in response:  
        return f"Error fetching portfolio performance: {response['error']}"  
    
    metrics = response.get("metrics", [])  
    
    if not metrics:  
        return f"No performance data found for portfolio {portfolio_id}."  
    
    result = f"Portfolio Performance & Risk Metrics for ID {portfolio_id}:\n\n"  
    
    # Group metrics by category  
    categories = {}  
    for metric in metrics:  
        category = metric.get("category", "Other")  
        if category not in categories:  
            categories[category] = []  
        categories[category].append(metric)  
    
    # Format metrics by category  
    for category, category_metrics in categories.items():  
        result += f"Category: {category}\n"  
        for metric in category_metrics:  
            result += f"  - {metric.get('name', 'Unknown')}: {metric.get('value', 'N/A')}\n"  
            result += f"    Description: {metric.get('description', 'No description')}\n"  
        result += "\n"  
    
    return result  

@mcp.tool()  
async def get_portfolio_sectors(portfolio_id: str, benchmark_id: str = None) -> str:  
    """Get sector breakdown for a portfolio."""  
    params = {  
        "portfolio_id": portfolio_id  
    }  
    
    if benchmark_id:  
        params["benchmark_id"] = benchmark_id  
    
    response = await make_dcsc_request("sectors", params)  
    
    if "error" in response:  
        return f"Error fetching portfolio sectors: {response['error']}"  
    
    sectors = response.get("sectors", [])  
    
    if not sectors:  
        return f"No sector data found for portfolio {portfolio_id}."  
    
    result = f"Sector Breakdown for Portfolio ID {portfolio_id}:\n\n"  
    
    formatted_sectors = [format_sector(sector) for sector in sectors]  
    return result + "\n---\n".join(formatted_sectors)  

@mcp.tool()  
async def get_classified_sectors(portfolio_id: str) -> str:  
    """Get AI-classified sectors for a portfolio."""  
    params = {  
        "portfolio_id": portfolio_id  
    }  
    
    response = await make_dcsc_request("classified_sectors", params)  
    
    if "error" in response:  
        return f"Error fetching classified sectors: {response['error']}"  
    
    sectors = response.get("sectors", [])  
    
    if not sectors:  
        return f"No classified sector data found for portfolio {portfolio_id}."  
    
    result = f"AI-Classified Sectors for Portfolio ID {portfolio_id}:\n\n"  
    
    formatted_sectors = [format_classified_sector(sector) for sector in sectors]  
    return result + "\n---\n".join(formatted_sectors)  

# Start the MCP server  
if __name__ == "__main__":  
    print("MCP running with CityFalcon and DCSC APIs")  
    # Initialize and run the server  
    mcp.run(transport='stdio')