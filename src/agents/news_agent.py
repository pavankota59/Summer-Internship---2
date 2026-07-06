import logging

logger = logging.getLogger(__name__)

def run_news_agent(ticker: str) -> dict:
    """
    News Agent stub. Pulls news from the last 7 days and tags sentiment.
    """
    logger.info(f"News Agent checking recent news for: {ticker}")
    return {
        "ticker": ticker,
        "digest": "No major news events in the last 7 days (stub output).",
        "items": []
    }
