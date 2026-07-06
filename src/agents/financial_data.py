import logging
from src.tools.yfinance_tool import fetch_financial_data

logger = logging.getLogger(__name__)

def format_financial_report(data: dict) -> str:
    """
    Formats the raw financial data dictionary into a professional markdown report
    satisfying the requirements of presenting precise numbers without personal bias.
    """
    if not data.get("success"):
        return f"### Financial Data Agent Report\n\n**Error**: {data.get('error', 'Unknown error occurred during retrieval')}"
        
    details = data["company_details"]
    ratios = data["ratios"]
    price = data["price_summary"]
    
    # Format currencies/numbers clearly for Indian or US markets
    def format_large_num(num):
        if num is None or num == "N/A":
            return "N/A"
        try:
            val = float(num)
            # Decide currency suffix based on ticker ending (.NS = INR, otherwise fallback generic)
            is_indian = details.get("symbol", "").endswith(".NS")
            currency_symbol = "₹" if is_indian else "$"
            
            if is_indian:
                if val >= 1e7:
                    return f"{currency_symbol}{val / 1e7:,.2f} Cr (Crores)"
                elif val >= 1e5:
                    return f"{currency_symbol}{val / 1e5:,.2f} L (Lakhs)"
                return f"{currency_symbol}{val:,.2f}"
            else:
                if val >= 1e12:
                    return f"{currency_symbol}{val / 1e12:,.2f} T (Trillion)"
                elif val >= 1e9:
                    return f"{currency_symbol}{val / 1e9:,.2f} B (Billion)"
                elif val >= 1e6:
                    return f"{currency_symbol}{val / 1e6:,.2f} M (Million)"
                return f"{currency_symbol}{val:,.2f}"
        except Exception:
            return str(num)

    def format_pct(num):
        if num is None or num == "N/A":
            return "N/A"
        try:
            val = float(num)
            # Check if percentage is stored as fraction (e.g. 0.05 instead of 5)
            # Operating metrics and growth values in yfinance info dictionary are typically fractional.
            if -1.0 <= val <= 1.0:
                val = val * 100
            return f"{val:.2f}%"
        except Exception:
            return str(num)

    def format_ratio(num):
        if num is None or num == "N/A":
            return "N/A"
        try:
            return f"{float(num):.2f}x"
        except Exception:
            return str(num)

    report = f"""# Equity Research Financial Report: {details['name']} ({details['symbol']})
**Sector**: {details['sector']} | **Industry**: {details['industry']}

## 1. Market & Price Performance Summary
- **Current Price**: {format_large_num(price.get('current_price'))}
- **52-Week High**: {format_large_num(price.get('fifty_two_week_high'))}
- **52-Week Low**: {format_large_num(price.get('fifty_two_week_low'))}
- **1-Year Price Return**: {format_pct(price.get('one_year_return_pct'))}

## 2. Key Valuation & Financial Ratios
- **Market Capitalization**: {format_large_num(ratios.get('market_cap'))}
- **Price-to-Earnings (P/E) Ratio**: {format_ratio(ratios.get('pe_ratio'))}
- **Price-to-Book (P/B) Ratio**: {format_ratio(ratios.get('pb_ratio'))}
- **EV/EBITDA**: {format_ratio(ratios.get('ev_ebitda'))}
- **Debt-to-Equity**: {format_ratio(ratios.get('debt_to_equity'))}
- **Profit Margin**: {format_pct(ratios.get('profit_margin'))}
- **Operating Margin**: {format_pct(ratios.get('operating_margin'))}
- **Revenue Growth (YoY)**: {format_pct(ratios.get('revenue_growth'))}
- **EBITDA Growth (YoY)**: {format_pct(ratios.get('ebitda_growth'))}

## 3. Business Description
{details['business_summary']}

---
**Disclaimer**: This report is compiled programmatically by the AlphaAgents Financial Data Agent node using public scraping endpoints and does not constitute certified financial advice.
"""
    return report.strip()

def run_financial_data_agent(ticker_symbol: str) -> dict:
    """
    Executes the Financial Data Agent node: fetches data, parses and formats the narrative report.
    
    Args:
        ticker_symbol (str): The stock ticker (e.g. 'TCS.NS', 'AAPL').
        
    Returns:
        dict: Final agent output format, containing success status, raw metrics, and formatted markdown report.
    """
    logger.info(f"Financial Data Agent starting process for ticker: {ticker_symbol}")
    raw_data = fetch_financial_data(ticker_symbol)
    
    if not raw_data.get("success"):
        return {
            "ticker": ticker_symbol,
            "success": False,
            "error": raw_data.get("error"),
            "markdown": f"Error running Financial Data Agent for {ticker_symbol}: {raw_data.get('error')}"
        }
        
    formatted_report = format_financial_report(raw_data)
    
    return {
        "ticker": ticker_symbol,
        "success": True,
        "raw_data": raw_data,
        "markdown": formatted_report
    }
