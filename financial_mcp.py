import asyncio  
from typing import Any, Dict, List, Optional  
import httpx  
from mcp.server.fastmcp import FastMCP  

mcp = FastMCP("financial-news")  

# CityFalcon API configuration  
API_KEY = ""
API_BASE_URL = "https://api.cityfalcon.com/v0.2"  

# Define headers without authorization (since we'll use query param for auth)  
HEADERS = {  
    "Content-Type": "application/json"  
}  

# Helper function to make API requests  
async def make_api_request(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:  
    url = f"{API_BASE_URL}/{endpoint}"  
    
    # Initialize params if None  
    if params is None:  
        params = {}  
    
    # Add access token to params instead of using Authorization header  
    params["access_token"] = API_KEY  
    
    async with httpx.AsyncClient() as client:  
        try:  
            response = await client.get(url, params=params, headers=HEADERS, timeout=30.0)  
            response.raise_for_status()  
            return response.json()  
        except Exception as e:  
            print(f"❌ Error making API request to {endpoint}: {e}")  
            return {"error": str(e)}

###################  
# FORMAT FUNCTIONS  
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
# STORIES ENDPOINTS  
###################  

@mcp.tool()  
async def get_news_by_ticker(ticker: str, limit: int = 5) -> str:  
    """Get latest financial news for a stock ticker."""  
    params = {  
        "identifier_type": "assets",  
        "identifiers": ticker,  
        "categories": "mp,op",  # Major and other news publications  
        "time_filter": "d1",    # Last 24 hours  
        "order_by": "latest",  
        "with_sentiment": True,  
        "limit": limit  
    }  
    
    response = await make_api_request("stories", params)  
    
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
        "categories": "mp,op",  
        "time_filter": "d1",  
        "order_by": "latest",  
        "with_sentiment": True,  
        "limit": limit  
    }  
    
    response = await make_api_request("stories", params)  
    
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
    
    response = await make_api_request(f"stories/{story_uuid}/similar_stories", params)  
    
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
    
    response = await make_api_request("stories/by_uuid", params)  
    
    if "error" in response:  
        return f"Error fetching stories: {response['error']}"  
    
    stories = response.get("stories", [])  
    
    if not stories:  
        return "No stories found for the provided UUIDs."  
    
    formatted_stories = [format_story(story) for story in stories]  
    return "\n---\n".join(formatted_stories)  

###################  
# SENTIMENT ENDPOINTS  
###################  

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
    
    response = await make_api_request("services/sentiment", params)  
    
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
    
    response = await make_api_request("services/entity_extraction", params)  
    
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

###################  
# ANALYST PRICE TARGETS  
###################  

@mcp.tool()  
async def get_analyst_price_targets(ticker: str) -> str:  
    """Get analyst price targets for a specific ticker."""  
    params = {  
        "identifier": ticker  
    }  
    
    response = await make_api_request("analyst_price_targets", params)  
    
    if "error" in response:  
        return f"Error fetching price targets: {response['error']}"  
    
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
    
    response = await make_api_request("analyst_price_targets/summary", params)  
    
    if "error" in response:  
        return f"Error fetching price targets summary: {response['error']}"  
    
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
    
    response = await make_api_request("analyst_price_targets/consensus", params)  
    
    if "error" in response:  
        return f"Error fetching price targets consensus: {response['error']}"  
    
    consensus = response.get("consensus", {})  
    
    result = f"Price targets consensus for {ticker}:\n\n"  
    result += f"Buy: {consensus.get('buy', 'N/A')}\n"  
    result += f"Overweight: {consensus.get('overweight', 'N/A')}\n"  
    result += f"Hold: {consensus.get('hold', 'N/A')}\n"  
    result += f"Underweight: {consensus.get('underweight', 'N/A')}\n"  
    result += f"Sell: {consensus.get('sell', 'N/A')}\n"  
    
    return result  

###################  
# FILINGS  
###################  

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
    
    response = await make_api_request("filings", params)  
    
    if "error" in response:  
        return f"Error fetching filings: {response['error']}"  
    
    filings = response.get("filings", [])  
    
    if not filings:  
        return f"No filings found for {identifiers} from {source}."  
    
    formatted_filings = [format_filing(filing) for filing in filings]  
    return f"Filings for {identifiers} from {source}:\n\n" + "\n---\n".join(formatted_filings)  

###################  
# INSIDER TRANSACTIONS  
###################  

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
    
    response = await make_api_request("insider_transactions", params)  
    
    if "error" in response:  
        return f"Error fetching insider transactions: {response['error']}"  
    
    transactions = response.get("transactions", [])  
    
    if not transactions:  
        return f"No insider transactions found for {identifiers}."  
    
    formatted_transactions = [format_insider_transaction(t) for t in transactions]  
    return f"Insider transactions for {identifiers}:\n\n" + "\n---\n".join(formatted_transactions)  

###################  
# INVESTOR RELATIONS  
###################  

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
    
    response = await make_api_request("investor_relations", params)  
    
    if "error" in response:  
        return f"Error fetching investor relations data: {response['error']}"  
    
    relations = response.get("relations", [])  
    
    if not relations:  
        return f"No investor relations data found for {identifiers}."  
    
    formatted_relations = [format_investor_relation(r) for r in relations]  
    return f"Investor relations for {identifiers}:\n\n" + "\n---\n".join(formatted_relations)  

###################  
# MARKET SUMMARY  
###################  

@mcp.tool()  
async def get_market_summary(identifiers: str, asset_class: str = "stocks") -> str:  
    """Get market summary for specified identifiers."""  
    params = {  
        "identifiers": identifiers,  
        "asset_class": asset_class  
    }  
    
    response = await make_api_request("market_summary", params)  
    
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
    
    response = await make_api_request("market_summary/performers", params)  
    
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

# Start the MCP server  
if __name__ == "__main__":  
    print("MCP running")  
    # Initialize and run the server  
    mcp.run(transport='stdio')