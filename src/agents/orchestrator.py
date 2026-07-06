import logging
import re

logger = logging.getLogger(__name__)

# Ticker lookup mappings for sample Indian large-caps
TICKER_MAP = {
    "reliance": "RELIANCE.NS",
    "tcs": "TCS.NS",
    "tata consultancy": "TCS.NS",
    "infosys": "INFY.NS",
    "infy": "INFY.NS"
}

def resolve_ticker(query: str) -> str:
    """
    Resolves a query into a stock ticker symbol.
    Uses regex and dictionary lookup. Defaults to TCS.NS if unresolved.
    """
    normalized = query.lower().strip()
    
    # Check if a ticker symbol (with or without .NS suffix) is directly provided
    match = re.search(r'\b([a-zA-Z0-9_\-\.]+)\b', normalized)
    if match:
        token = match.group(1)
        # Directly match against common keys
        for key, val in TICKER_MAP.items():
            if key in token:
                return val
        if token.endswith(".ns") or len(token) >= 3 and token.isupper():
            return token.upper()
            
    # Substring search
    for key, val in TICKER_MAP.items():
        if key in normalized:
            return val
            
    # Default fallback
    logger.warning(f"Could not resolve ticker for query '{query}'. Falling back to TCS.NS.")
    return "TCS.NS"

def run_orchestrator(company_query: str) -> dict:
    """
    Orchestrates the research plan: parses queries, resolves the ticker symbol,
    and structures the sub-questions to send to the worker agents.
    
    Args:
        company_query (str): User research query (e.g. 'Analyze Reliance Industries').
        
    Returns:
        dict: A structured research plan containing the resolved ticker and sub-questions.
    """
    logger.info(f"Orchestrator building plan for query: {company_query}")
    resolved_sym = resolve_ticker(company_query)
    
    # 4 mandatory sub-questions per the E1 problem statement roadmap
    sub_questions = [
        {
            "id": 1,
            "question": f"What is {resolved_sym}'s current financial health, growth, and key metrics?",
            "assigned_agent": "financial_data_agent"
        },
        {
            "id": 2,
            "question": f"What are the major news articles or press releases for {resolved_sym} over the last 7 days?",
            "assigned_agent": "news_agent"
        },
        {
            "id": 3,
            "question": f"Who are the key competitors of {resolved_sym} and how does the company compare to them?",
            "assigned_agent": "web_researcher_agent"
        },
        {
            "id": 4,
            "question": f"What is a fair valuation range for {resolved_sym} given its current ratios?",
            "assigned_agent": "financial_data_agent"
        }
    ]
    
    return {
        "query": company_query,
        "ticker": resolved_sym,
        "sub_questions": sub_questions
    }
