import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import sys
import os

# Adjust path to resolve imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.yfinance_tool import fetch_financial_data

class TestYFinanceTool(unittest.TestCase):
    
    @patch('src.tools.yfinance_tool.yf.Ticker')
    def test_fetch_financial_data_success(self, mock_ticker):
        """
        Verify that fetch_financial_data returns structured details, key ratios,
        and pricing summary when yfinance successfully returns stock information.
        """
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        
        # Set up mock info dictionary
        mock_instance.info = {
            "symbol": "TCS.NS",
            "longName": "Tata Consultancy Services Limited",
            "sector": "Technology",
            "industry": "Information Technology Services",
            "longBusinessSummary": "Leading global IT services provider.",
            "marketCap": 14000000000000,
            "trailingPE": 30.5,
            "priceToBook": 12.4,
            "enterpriseToEbitda": 20.2,
            "debtToEquity": 8.5,
            "profitMargins": 0.195,
            "operatingMargins": 0.245,
            "revenueGrowth": 0.082,
            "ebitdaGrowth": 0.075,
            "currentPrice": 3950.0
        }
        
        # Set up mock history DataFrame
        mock_history = pd.DataFrame({
            "Open": [3900.0, 3940.0],
            "High": [3950.0, 3980.0],
            "Low": [3890.0, 3920.0],
            "Close": [3930.0, 3950.0],
            "Volume": [1000, 2000]
        })
        mock_instance.history.return_value = mock_history
        
        # Run function
        result = fetch_financial_data("TCS.NS")
        
        # Assertions
        self.assertTrue(result["success"])
        self.assertEqual(result["company_details"]["symbol"], "TCS.NS")
        self.assertEqual(result["company_details"]["name"], "Tata Consultancy Services Limited")
        self.assertEqual(result["ratios"]["pe_ratio"], 30.5)
        self.assertEqual(result["price_summary"]["current_price"], 3950.0)
        self.assertEqual(result["price_summary"]["fifty_two_week_high"], 3980.0)
        self.assertEqual(result["price_summary"]["fifty_two_week_low"], 3890.0)

    @patch('src.tools.yfinance_tool.yf.Ticker')
    def test_fetch_financial_data_invalid_ticker(self, mock_ticker):
        """
        Verify that fetch_financial_data safely returns an error dict if yfinance info is empty.
        """
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        
        # Empty info represents invalid ticker symbol
        mock_instance.info = {}
        
        # Run function
        result = fetch_financial_data("INVALID")
        
        # Assertions
        self.assertFalse(result["success"])
        self.assertIn("verify the symbol", result["error"])

if __name__ == '__main__':
    unittest.main()
