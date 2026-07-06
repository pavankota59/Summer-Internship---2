# Data Sources

This document describes the API and data sources integrated into the AlphaAgents research pipeline.

## 1. yfinance (Financial Data Agent)
- **Purpose**: Retrieves historical pricing, valuation metrics, capital structure, and fundamental financial ratios for the target equity.
- **Access**: Free, open-source library that scrapes Yahoo Finance. No API key required.
- **Ratios Extracted**:
  - P/E (Price-to-Earnings) Ratio
  - P/B (Price-to-Book) Ratio
  - EV/EBITDA
  - Debt-to-Equity Ratio
  - Profit Margins & Operating Margins
  - Revenue Growth & EBITDA Growth
- **Limitations**: Scraped data may have minor delays (15-20 minutes) or occasional omissions for smaller tickers.

## 2. Tavily Search API (Web Researcher Agent)
- **Purpose**: Executes web searches optimized for LLMs to find industry news, competitive analyses, and strategic developments.
- **Access**: Free tier API key (requires signup).
- **Output**: Returns relevant page content snippets, clean HTML extracts, and source URLs.

## 3. NewsAPI (News Agent)
- **Purpose**: Fetches business headlines and news articles from the last 7 days to evaluate short-term sentiment and corporate events.
- **Access**: Free tier API key (requires signup, limited to 100 requests per day).
- **Scope**: Focused on reputable financial news outlets (e.g., Bloomberg, Reuters, Economic Times).
