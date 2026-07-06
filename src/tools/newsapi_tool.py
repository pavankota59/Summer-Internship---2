import os
import logging
import requests
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Predefined mock news events for last 7 days
MOCK_NEWS_DATA = {
    "RELIANCE.NS": [
        {
            "source": "Economic Times",
            "title": "Reliance Industries expansion into green hydrogen facilities",
            "description": "Reliance details investment plan for new clean energy solar and green hydrogen giga-factories in Gujarat.",
            "url": "https://economictimes.indiatimes.com/reliance-green-hydrogen",
            "published_at": "2026-07-03T10:00:00Z"
        },
        {
            "source": "Bloomberg",
            "title": "Jio Platforms announces revised subscription tariff structure",
            "description": "Reliance Jio increases cellular pricing plans by 12-15% to boost average revenue per user (ARPU).",
            "url": "https://www.bloomberg.com/jio-tariff-hike",
            "published_at": "2026-07-05T08:30:00Z"
        }
    ],
    "TCS.NS": [
        {
            "source": "Reuters",
            "title": "TCS bags mega $1.5 billion deal in UK insurance sector",
            "description": "Tata Consultancy Services secures a long-term core transformation contract with a UK financial client.",
            "url": "https://www.reuters.com/tcs-uk-insurance-deal",
            "published_at": "2026-07-02T14:15:00Z"
        },
        {
            "source": "Business Standard",
            "title": "TCS attrition stabilizes as software industry hiring slows",
            "description": "Attrition levels drop to 12.1% at TCS, reflecting stabilization in enterprise employee turnover.",
            "url": "https://www.business-standard.com/tcs-attrition-levels",
            "published_at": "2026-07-04T11:45:00Z"
        }
    ],
    "INFY.NS": [
        {
            "source": "TechCrunch",
            "title": "Infosys expands global AI collaboration with NVIDIA",
            "description": "Infosys expands partnership to build generative AI solutions for telecommunications and retail enterprises.",
            "url": "https://techcrunch.com/infosys-nvidia-alliance",
            "published_at": "2026-07-01T09:00:00Z"
        },
        {
            "source": "Mint",
            "title": "Infosys signs $800M cloud transition deal with European retailer",
            "description": "Infosys to transform digital retail infrastructure using Cobalt cloud suite services.",
            "url": "https://livemint.com/infosys-800m-retail-contract",
            "published_at": "2026-07-06T06:00:00Z"
        }
    ]
}

def fetch_recent_news(query: str, ticker: str = None) -> list:
    """
    Fetches news articles from the last 7 days matching a query.
    If the API key is missing or calls fail, it falls back to mock news.
    
    Args:
        query (str): Query term (e.g. 'Reliance').
        ticker (str, optional): Resolved ticker symbol to assist mock matching.
        
    Returns:
        list: A list of news articles containing source, title, description, url, and published date.
    """
    api_key = os.getenv("NEWS_API_KEY")
    
    if not api_key:
        logger.warning("NEWS_API_KEY not found. Returning mock news dataset.")
        return _get_mock_news(query, ticker)
        
    try:
        logger.info(f"Calling NewsAPI for query: {query}")
        # Restrict search to last 7 days
        seven_days_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "from": seven_days_ago,
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": api_key,
            "pageSize": 5
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            news_items = []
            for art in articles:
                news_items.append({
                    "source": art.get("source", {}).get("name", "Unknown Source"),
                    "title": art.get("title", ""),
                    "description": art.get("description", ""),
                    "url": art.get("url", "#"),
                    "published_at": art.get("publishedAt", "")
                })
            return news_items
        else:
            logger.warning(f"NewsAPI error {response.status_code}: {response.text}. Using fallback.")
            return _get_mock_news(query, ticker)
            
    except Exception as e:
        logger.error(f"Failed to fetch NewsAPI data: {e}. Using fallback.")
        return _get_mock_news(query, ticker)

def _get_mock_news(query: str, ticker: str = None) -> list:
    """
    Retrieves mock news articles based on query terms or ticker.
    """
    normalized_query = query.lower()
    
    # Try match by ticker first
    if ticker and ticker in MOCK_NEWS_DATA:
        return MOCK_NEWS_DATA[ticker]
        
    # Match query strings
    if "reliance" in normalized_query:
        return MOCK_NEWS_DATA["RELIANCE.NS"]
    elif "tcs" in normalized_query or "tata consultancy" in normalized_query:
        return MOCK_NEWS_DATA["TCS.NS"]
    elif "infosys" in normalized_query or "infy" in normalized_query:
        return MOCK_NEWS_DATA["INFY.NS"]
        
    # Generic fallback news
    return [
        {
            "source": "Financial Digest",
            "title": f"Recent operational developments at {query}",
            "description": f"Industry reports mention strategic changes at {query} with steady corporate updates reported in global journals.",
            "url": "https://www.example.com/finance-news",
            "published_at": (datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    ]
