import sys
import os

# Add the project root to python path to resolve src imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.financial_data import run_financial_data_agent

def main():
    # Tickers across Indian large-caps
    tickers = ["RELIANCE.NS", "TCS.NS", "TATAMOTORS.NS"]
    
    print("=" * 70)
    print("ALPHAGENTS — FINANCIAL DATA AGENT VERIFICATION RUN")
    print("=" * 70)
    
    for ticker in tickers:
        print(f"\nExecuting analysis node for ticker: {ticker} ...")
        result = run_financial_data_agent(ticker)
        
        if result["success"]:
            print(f"\n[SUCCESS] Compiled financial data report for {ticker}:\n")
            print(result["markdown"])
        else:
            print(f"\n[FAILED] Could not execute for {ticker}. Error: {result.get('error')}")
        print("-" * 70)

if __name__ == "__main__":
    main()
