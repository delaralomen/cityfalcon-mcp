import asyncio  
import os  
from datetime import datetime  
from tqdm import tqdm  

# Import the functions from financial_mcp.py  
from financial_mcp import (  
    # CityFalcon API functions  
    get_news_by_ticker_or_topic, 
    get_similar_stories,  
    get_stories_by_uuid,  
    get_entity_sentiment,
    get_analyst_price_targets,  
    get_price_targets_summary,  
    get_price_targets_consensus, 
    get_insider_transactions, 
    # DCSC API functions (corrected)
    list_sectors,
    get_sector_hierarchy,
    get_smart_portfolio,
    get_portfolio_classification,
    get_portfolio_performance_risk,
    get_classified_sectors_mapping,
    # Help function
    list_available_capabilities
)  

# Setup log file  
log_dir = "logs"  
os.makedirs(log_dir, exist_ok=True)  
log_filename = f"{log_dir}/financial_mcp_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"  

# Open log file for writing  
log_file = open(log_filename, "w", encoding="utf-8")  

def write_to_log(message):  
    """Write message to log file with timestamp"""  
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
    log_file.write(f"[{timestamp}] {message}\n")  
    log_file.flush()  # Ensure it's written immediately  

# Test case definition - maps function to its test parameters  
test_cases = [  
    # CityFalcon API Tests  
    {"func": get_news_by_ticker_or_topic, "params": {"ticker": "AAPL", "limit": 3}},  
    {"func": get_news_by_ticker_or_topic, "params": {"ticker": "MSFT", "limit": 3}},  
    {"func": get_news_by_ticker_or_topic, "params": {"ticker": "GOOGL", "limit": 3}},
    {"func": get_news_by_ticker_or_topic, "params": {"ticker": "inflation", "limit": 3}}, 
    {"func": get_news_by_ticker_or_topic, "params": {"ticker": "federal reserve system", "limit": 3}}, 
    # The following test needs a valid UUID - you'll need to get one from a previous call  
    # {"func": get_similar_stories, "params": {"story_uuid": "EXAMPLE_UUID", "limit": 3}},  
    # {"func": get_stories_by_uuid, "params": {"uuids": "UUID1,UUID2"}},  
    {"func": get_entity_sentiment, "params": {"identifiers": "stocks", "period": "d1"}},  
    {"func": get_entity_sentiment, "params": {"identifiers": "bonds", "period": "w1"}},  
    {"func": get_analyst_price_targets, "params": {"ticker": "AAPL"}},  
    {"func": get_analyst_price_targets, "params": {"ticker": "TSLA"}},  
    {"func": get_price_targets_summary, "params": {"ticker": "AAPL"}},  
    {"func": get_price_targets_summary, "params": {"ticker": "MSFT"}},  
    {"func": get_price_targets_consensus, "params": {"ticker": "AAPL"}},  
    {"func": get_price_targets_consensus, "params": {"ticker": "AMZN"}},  
    {"func": get_insider_transactions, "params": {"identifiers": "AAPL", "per_page": 3}},  
    {"func": get_insider_transactions, "params": {"identifiers": "AMZN", "per_page": 3}},
    
    # DCSC API Tests (corrected)
    {"func": list_sectors, "params": {}},
    
    # Note: The following tests may fail if we don't have valid sector slugs
    # You should run list_sectors first to get actual slugs, then update these tests
    {"func": get_sector_hierarchy, "params": {"level": 1, "slug": "technology"}, "skip": True},  # Skip until we get valid slugs
    
    {"func": get_smart_portfolio, "params": {
        "level": 1,
        "slugs": "technology",
        "max_securities": 5,
        "min_relevance": 10,
        "company_type": "public"
    }, "skip": True},  # Skip until we get valid slugs
    
    {"func": get_portfolio_classification, "params": {
        "identifiers": "AAPL,MSFT,GOOGL",
        "identifier_type": "ticker",
        "allocation": "40,30,30",
        "min_relevance": 10
    }},
    
    {"func": get_portfolio_performance_risk, "params": {
        "identifiers": "AAPL,MSFT",
        "identifier_type": "ticker",
        "allocation": "50,50",
        "period": "1y"
    }},
    
    {"func": get_classified_sectors_mapping, "params": {
        "classification_name": "NAICS",
        "sector_number": "5112"
    }},
    
    {"func": get_classified_sectors_mapping, "params": {
        "classification_name": "GICS",
        "sector_name": "Information Technology"
    }},
    
    # Help function test
    {"func": list_available_capabilities, "params": {}},
]  

async def run_test_case(test_case):  
    """Run a test case and return result with status"""  
    func = test_case["func"]  
    params = test_case["params"]  
    skip = test_case.get("skip", False)  
    
    # Log test start  
    write_to_log(f"==== STARTING TEST: {func.__name__} ====")  
    write_to_log(f"Parameters: {params}")  
    
    if skip:  
        write_to_log(f"Test skipped: {func.__name__}")  
        return {  
            "function": func.__name__,  
            "params": params,  
            "status": "SKIPPED",  
            "result": None,  
            "error": None  
        }  
    
    try:  
        result = await func(**params)  
        error_indicators = ["Error fetching", "HTTP error", "403", "404", "401", "400", "500"]  
        
        # Check for error messages in the result  
        if any(indicator in result for indicator in error_indicators):  
            write_to_log(f"Test FAILED: {func.__name__}")  
            write_to_log(f"Error detected in response: {result}")  
            return {  
                "function": func.__name__,  
                "params": params,  
                "status": "FAILED",  
                "result": result,  
                "error": "Found error indicator in response"  
            }  
        
        # Log successful result with full output  
        write_to_log(f"Test PASSED: {func.__name__}")  
        write_to_log(f"Result:\n{result}\n")  
        
        return {  
            "function": func.__name__,  
            "params": params,  
            "status": "PASSED",  
            "result": result,  
            "error": None  
        }  
    except Exception as e:  
        write_to_log(f"Test ERROR: {func.__name__}")  
        write_to_log(f"Exception: {str(e)}")  
        return {  
            "function": func.__name__,  
            "params": params,  
            "status": "ERROR",  
            "result": None,  
            "error": str(e)  
        }  
    finally:  
        write_to_log(f"==== COMPLETED TEST: {func.__name__} ====\n")  

async def run_all_tests():  
    """Run all test cases with progress bar"""  
    results = []  
    
    write_to_log("========================================")  
    write_to_log("STARTING FINANCIAL MCP API TESTS")  
    write_to_log("========================================")  
    
    # Setup progress bar  
    with tqdm(total=len(test_cases), desc="Running API Tests", unit="test") as progress_bar:  
        for test_case in test_cases:  
            # Run the test  
            result = await run_test_case(test_case)  
            results.append(result)  
            
            # Only show minimal info in progress bar  
            status_chars = {"PASSED": "✅", "FAILED": "❌", "ERROR": "❌", "SKIPPED": "⏭️"}  
            progress_bar.set_postfix_str(f"{status_chars[result['status']]} {result['function']}")  
            progress_bar.update(1)  
    
    write_to_log("========================================")  
    write_to_log("ALL TESTS COMPLETED")  
    write_to_log("========================================")  
    
    return results  

def print_summary(results):  
    """Print summary of test results"""  
    total = len(results)  
    passed = sum(1 for r in results if r["status"] == "PASSED")  
    failed = sum(1 for r in results if r["status"] == "FAILED")  
    errors = sum(1 for r in results if r["status"] == "ERROR")  
    skipped = sum(1 for r in results if r["status"] == "SKIPPED")  
    
    success_rate = (passed / (total - skipped)) * 100 if (total - skipped) > 0 else 0  
    
    summary = f"""  
{'='*50}  
FINANCIAL MCP TEST SUMMARY  
{'='*50}  
Total Tests: {total}  
Passed: {passed} ({success_rate:.1f}%)  
Failed: {failed}  
Errors: {errors}  
Skipped: {skipped}  
{'='*50}  
Detailed logs written to: {log_filename}  

NOTE: Some DCSC tests are skipped because they require valid sector slugs.
Run list_sectors() first to get actual slugs, then update the test parameters.
"""  
    
    print(summary)  
    write_to_log(summary)  
    
    # Print failed tests  
    if failed > 0 or errors > 0:  
        failed_summary = "\nFailed/Error Tests:"  
        for r in results:  
            if r["status"] in ["FAILED", "ERROR"]:  
                error_msg = f"- {r['function']} ({r['status']}): {r['error']}"  
                failed_summary += f"\n{error_msg}"  
        
        print(failed_summary)  
        write_to_log(failed_summary)  

if __name__ == "__main__":  
    # Run tests and print summary  
    print("Starting Financial MCP API tests...")  
    try:  
        results = asyncio.run(run_all_tests())  
        print_summary(results)  
    except Exception as e:  
        error_msg = f"Test runner exception: {str(e)}"  
        print(error_msg)  
        write_to_log(error_msg)  
    finally:  
        # Close log file  
        if log_file:  
            log_file.close()  
            print(f"Log file closed: {log_filename}")