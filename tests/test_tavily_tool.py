import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.tavily_tool import search_web

class TestTavilyTool(unittest.TestCase):
    
    @patch.dict(os.environ, {"TAVILY_API_KEY": "test_tavily_key"})
    @patch('src.tools.tavily_tool.TavilyClient')
    def test_search_web_api_success(self, mock_client_class):
        """
        Verify that search_web calls the Tavily Client search method and returns
        standardized results when an API key is provided and the request succeeds.
        """
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # Simulated Tavily response format
        mock_client.search.return_value = {
            "results": [
                {
                    "title": "TCS Market Outlook",
                    "url": "https://example.com/tcs",
                    "content": "TCS growth in digital business services.",
                    "score": 0.99
                }
            ]
        }
        
        results = search_web("TCS competitors")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "TCS Market Outlook")
        self.assertEqual(results[0]["url"], "https://example.com/tcs")
        self.assertEqual(results[0]["content"], "TCS growth in digital business services.")
        self.assertEqual(results[0]["published_date"], "2026-07-01") # Default fallback date
        mock_client.search.assert_called_once_with(query="TCS competitors", max_results=3)

    @patch.dict(os.environ, {}, clear=True)
    def test_search_web_fallback_when_no_key(self):
        """
        Verify that search_web falls back to pre-defined mock datasets when
        no TAVILY_API_KEY is found in the environment.
        """
        # Search containing 'reliance' keyword to trigger mock reliance dataset
        results = search_web("reliance business model")
        
        self.assertTrue(len(results) > 0)
        # Verify it resolves to Reliance mock details
        self.assertIn("reliance", results[0]["url"])
        self.assertIn("Reliance", results[0]["title"])

if __name__ == '__main__':
    unittest.main()
