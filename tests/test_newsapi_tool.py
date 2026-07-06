import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.newsapi_tool import fetch_recent_news

class TestNewsApiTool(unittest.TestCase):
    
    @patch.dict(os.environ, {"NEWS_API_KEY": "test_news_key"})
    @patch('src.tools.newsapi_tool.requests.get')
    def test_fetch_recent_news_success(self, mock_get):
        """
        Verify that fetch_recent_news issues a GET request to NewsAPI and
        parses articles properly when the API key is configured.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "articles": [
                {
                    "source": {"name": "TechCrunch"},
                    "title": "Infosys AI announcement",
                    "description": "Infosys integrates new generative AI nodes.",
                    "url": "https://techcrunch.com/infosys",
                    "publishedAt": "2026-07-06T12:00:00Z"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        results = fetch_recent_news("Infosys")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["source"], "TechCrunch")
        self.assertEqual(results[0]["title"], "Infosys AI announcement")
        self.assertEqual(results[0]["url"], "https://techcrunch.com/infosys")
        self.assertTrue(mock_get.called)

    @patch.dict(os.environ, {}, clear=True)
    def test_fetch_recent_news_fallback_when_no_key(self):
        """
        Verify that fetch_recent_news falls back to mock news files when
        no NEWS_API_KEY is found in the environment.
        """
        results = fetch_recent_news("TCS")
        
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["source"], "Reuters")
        self.assertIn("TCS", results[0]["title"])

if __name__ == '__main__':
    unittest.main()
