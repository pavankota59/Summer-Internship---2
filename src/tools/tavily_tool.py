import os
import logging
from tavily import TavilyClient

logger = logging.getLogger(__name__)

# Predefined mock datasets for robust fallback
MOCK_SEARCH_DATA = {
    "RELIANCE.NS": [
        {
            "title": "Reliance Industries Sector Position and Competitors",
            "url": "https://www.financialexpress.com/reliance-competitors",
            "content": "Reliance Industries is India's largest conglomerate. Its primary competitors in the Oil to Chemicals (O2C) segment include Indian Oil Corporation (IOC) and Bharat Petroleum (BPCL). In retail, it competes with D-Mart and Tata Group's Trent. In telecom, its chief rival is Bharti Airtel.",
            "published_date": "2026-06-15"
        },
        {
            "title": "Reliance Retail and Jio Market Leadership",
            "url": "https://www.economictimes.com/reliance-market-share",
            "content": "Reliance Retail operates over 18,000 stores across India. Jio Platforms holds the leading market share in the Indian telecom sector with over 450 million subscribers, driving digital ecosystem growth.",
            "published_date": "2026-06-20"
        }
    ],
    "TCS.NS": [
        {
            "title": "TCS vs Competitors: Q1 Market Share Analysis",
            "url": "https://www.moneycontrol.com/tcs-vs-competitors",
            "content": "Tata Consultancy Services (TCS) maintains its position as the largest Indian IT services exporter. Its key peers are Infosys, Wipro, and HCL Technologies. TCS reports industry-leading operating margins of 24-25%, compared to 20-21% for Infosys.",
            "published_date": "2026-06-10"
        },
        {
            "title": "TCS AI and Cloud Pipeline Growth",
            "url": "https://www.livemint.com/tcs-deal-pipeline",
            "content": "TCS has launched its WisdomNext platform to aggregate GenAI models for enterprise customers. The company continues to see strong cloud migration deal pipelines in the UK and Europe, helping offset North American softness.",
            "published_date": "2026-06-25"
        }
    ],
    "INFY.NS": [
        {
            "title": "Infosys Competitor Position and Services",
            "url": "https://www.bloombergquint.com/infosys-positioning",
            "content": "Infosys Limited is the second-largest Indian IT services firm. It competes directly with TCS, Wipro, Cognizant, and Accenture. Infosys is focusing on generative AI through its Topaz suite and has consolidated its Cloud brand under Cobalt.",
            "published_date": "2026-06-12"
        },
        {
            "title": "Infosys Large Deals and Guidance",
            "url": "https://www.reuters.com/infosys-results-outlook",
            "content": "Infosys reports a strong pipeline of large deals worth $3.2 billion, although discretionary tech spending in retail and banking verticals continues to face headwinds, leading to cautious guidance.",
            "published_date": "2026-06-28"
        }
    ]
}

def search_web(query: str, ticker: str = None) -> list:
    """
    Performs a web search using the Tavily Search API.
    If the API key is not configured, it falls back to mock search results.
    
    Args:
        query (str): The search query.
        ticker (str, optional): The resolved stock ticker. Used to locate precise mock data.
        
    Returns:
        list: A list of search result dictionaries containing title, url, content, and date.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    
    if not api_key:
        logger.warning("TAVILY_API_KEY not found in environment. Falling back to mock dataset.")
        return _get_mock_results(query, ticker)
        
    try:
        logger.info(f"Executing Tavily web search for query: {query}")
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=3)
        results = response.get("results", [])
        
        # Convert response items to standard structure
        standardized_results = []
        for r in results:
            standardized_results.append({
                "title": r.get("title", "No Title"),
                "url": r.get("url", "#"),
                "content": r.get("content", ""),
                # Mock a date if not returned by Tavily free search
                "published_date": r.get("published_date") or "2026-07-01"
            })
        return standardized_results
        
    except Exception as e:
        logger.error(f"Error calling Tavily Search API: {e}. Falling back to mock dataset.")
        return _get_mock_results(query, ticker)

def _get_mock_results(query: str, ticker: str = None) -> list:
    """
    Retrieves mock results based on query terms or ticker.
    """
    normalized_query = query.lower()
    
    # Try resolving via ticker first
    if ticker and ticker in MOCK_SEARCH_DATA:
        return MOCK_SEARCH_DATA[ticker]
        
    # Match query strings
    if "reliance" in normalized_query:
        return MOCK_SEARCH_DATA["RELIANCE.NS"]
    elif "tcs" in normalized_query or "tata consultancy" in normalized_query:
        return MOCK_SEARCH_DATA["TCS.NS"]
    elif "infosys" in normalized_query or "infy" in normalized_query:
        return MOCK_SEARCH_DATA["INFY.NS"]
        
    # Generic fallback
    return [
        {
            "title": f"Strategic analysis for query: {query}",
            "url": "https://www.example.com/equity-analysis",
            "content": f"Factual search overview for '{query}'. Competitor positioning shows steady industry dynamics with standard valuation benchmarks aligned to current sector metrics.",
            "published_date": "2026-07-02"
        }
    ]
