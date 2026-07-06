import logging
from src.tools.newsapi_tool import fetch_recent_news

logger = logging.getLogger(__name__)

def evaluate_relevance_and_sentiment(title: str, desc: str) -> tuple:
    """
    Tags news items with relevance (High, Medium, Low) and simple sentiment indicators
    based on key operational indicators.
    """
    text = (title + " " + desc).lower()
    
    # Simple heuristic indicators for operational importance
    high_impact_keywords = ["hydrogen", "acquisition", "billion", "tariff", "deal", "contract", "earnings", "profit", "margin", "nvidia", "partnership"]
    medium_impact_keywords = ["expansion", "hiring", "attrition", "launch", "stability", "agreement"]
    
    sentiment = "Neutral"
    if any(pos in text for pos in ["growth", "expansion", "deal", "bagged", "secures", "revised", "partnership", "stabilizes"]):
        sentiment = "Positive"
    elif any(neg in text for neg in ["headwinds", "slows", "caution", "drop", "decline", "layoff"]):
        sentiment = "Cautious"
        
    relevance = "Low"
    if any(hk in text for hk in high_impact_keywords):
        relevance = "High"
    elif any(mk in text for mk in medium_impact_keywords):
        relevance = "Medium"
        
    return relevance, sentiment

def run_news_agent(ticker: str) -> dict:
    """
    Executes the News Agent task. Pulls news from the last 7 days for the ticker
    and generates a structured markdown news digest with impact tags.
    
    Args:
        ticker (str): Resolved ticker symbol.
        
    Returns:
        dict: A digest summary, structured items list, and success status.
    """
    logger.info(f"News Agent checking news digest for ticker: {ticker}")
    articles = fetch_recent_news(ticker, ticker)
    
    if not articles:
        return {
            "success": True,
            "digest": "No material news identified in the review window.",
            "items": []
        }
        
    digest_parts = []
    digest_parts.append("### Recent News & Sentiment Analysis (Last 7 Days)")
    
    structured_items = []
    for art in articles:
        title = art.get("title", "News Headline")
        desc = art.get("description", "No description available.")
        source = art.get("source", "Publisher")
        pub_time = art.get("published_at", "")
        url = art.get("url", "#")
        
        # Simple evaluation logic
        relevance, sentiment = evaluate_relevance_and_sentiment(title, desc)
        
        # Structure item
        item = {
            "title": title,
            "source": source,
            "date": pub_time[:10] if pub_time else "N/A",
            "url": url,
            "relevance": relevance,
            "sentiment": sentiment
        }
        structured_items.append(item)
        
        digest_parts.append(
            f"- **{title}**\n"
            f"  - *Publisher*: {source} | *Date*: {pub_time[:10]}\n"
            f"  - *Impact Relevance*: **{relevance}** | *Sentiment*: **{sentiment}**\n"
            f"  - *Summary*: {desc}"
        )
        
    digest_text = "\n\n".join(digest_parts)
    
    return {
        "success": True,
        "digest": digest_text,
        "items": structured_items
    }
