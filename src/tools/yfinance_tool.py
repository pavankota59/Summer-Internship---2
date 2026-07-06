import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def fetch_financial_data(ticker_symbol: str) -> dict:
    """
    Fetches core financial fundamentals, ratios, and historical price summary
    for a given stock ticker symbol using yfinance.
    
    Args:
        ticker_symbol (str): The stock ticker (e.g., 'TCS.NS', 'RELIANCE.NS', 'AAPL').
        
    Returns:
        dict: A dictionary containing status, company details, key ratios, and price summary.
    """
    try:
        logger.info(f"Initiating financial data fetch for ticker: {ticker_symbol}")
        ticker = yf.Ticker(ticker_symbol)
        
        # Safely attempt to access the info dictionary
        info = ticker.info
        
        # yfinance sometimes returns an empty dict or a dict with no key data if ticker is invalid
        if not info or (not info.get('symbol') and not info.get('shortName')):
            logger.warning(f"No valid information returned from yfinance for ticker: {ticker_symbol}")
            return {
                "success": False,
                "error": f"No data found for ticker '{ticker_symbol}'. Please verify the symbol."
            }
        
        # 1. Company General Details
        company_details = {
            "symbol": info.get("symbol", ticker_symbol),
            "name": info.get("longName") or info.get("shortName") or "N/A",
            "sector": info.get("sector") or "N/A",
            "industry": info.get("industry") or "N/A",
            "business_summary": info.get("longBusinessSummary") or "N/A"
        }
        
        # 2. Key Valuation & Leverage Ratios
        ratios = {
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE") or info.get("forwardPE"),
            "pb_ratio": info.get("priceToBook"),
            "ev_ebitda": info.get("enterpriseToEbitda"),
            "debt_to_equity": info.get("debtToEquity"),
            "profit_margin": info.get("profitMargins"),
            "operating_margin": info.get("operatingMargins"),
            "revenue_growth": info.get("revenueGrowth"),
            "ebitda_growth": info.get("ebitdaGrowth")
        }
        
        # 3. Price Performance (1 Year)
        price_summary = {}
        try:
            hist = ticker.history(period="1y")
            if not hist.empty:
                current_price = info.get("currentPrice")
                if not current_price:
                    # Fallback to last close if currentPrice isn't in info
                    current_price = float(hist['Close'].iloc[-1])
                
                price_summary = {
                    "current_price": current_price,
                    "fifty_two_week_high": float(hist['High'].max()),
                    "fifty_two_week_low": float(hist['Low'].min()),
                    "one_year_return_pct": float(((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100)
                }
            else:
                logger.warning(f"History dataframe was empty for ticker: {ticker_symbol}")
                price_summary = {
                    "current_price": info.get("currentPrice") or "N/A",
                    "fifty_two_week_high": info.get("fiftyTwoWeekHigh") or "N/A",
                    "fifty_two_week_low": info.get("fiftyTwoWeekLow") or "N/A",
                    "one_year_return_pct": "N/A"
                }
        except Exception as hist_err:
            logger.error(f"Failed to fetch historical pricing for {ticker_symbol}: {hist_err}")
            price_summary = {
                "current_price": info.get("currentPrice") or "N/A",
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh") or "N/A",
                "fifty_two_week_low": info.get("fiftyTwoWeekLow") or "N/A",
                "one_year_return_pct": "N/A"
            }
            
        return {
            "success": True,
            "company_details": company_details,
            "ratios": ratios,
            "price_summary": price_summary
        }
    except Exception as e:
        logger.error(f"Critical error fetching data for {ticker_symbol}: {e}", exc_info=True)
        return {
            "success": False,
            "error": f"Critical retrieval error: {str(e)}"
        }
