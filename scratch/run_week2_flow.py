import sys
import os

# Add root folder to python path to resolve src imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import app_graph

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run LangGraph Equity Research workflow.")
    parser.add_argument("--query", type=str, default="Analyze Reliance Industries", help="Query ticker or name")
    args = parser.parse_args()
    
    # Configure stdout to use utf-8 encoding to avoid Windows cp1252 printing errors
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
        
    print("=" * 80)
    print(f"RUNNING LANGGRAPH WEEK 2 FLOW FOR QUERY: '{args.query}'")
    print("=" * 80)
    
    # Initialize state dictionary conforming to state schema
    initial_state = {
        "query": args.query,
        "ticker": "",
        "financial_data": {},
        "web_research": [],
        "news_data": {},
        "draft": "",
        "critic_feedback": [],
        "critic_verdict": "",
        "loop_count": 0,
        "published": False
    }
    
    try:
        # Stream the graph updates
        for event in app_graph.stream(initial_state):
            for node_name, state_update in event.items():
                print(f"\n[NODE COMPLETED] ---> {node_name}")
                for key, val in state_update.items():
                    print(f"  * State Key Updated: '{key}'")
                    
                    if key == "ticker":
                        print(f"    -> Resolved Ticker: {val}")
                    elif key == "financial_data":
                        print(f"    -> Status: {'Success' if val.get('success') else 'Fail'}")
                        if val.get("success"):
                            # Print a snippet of the markdown report
                            lines = val["markdown"].split("\n")
                            print(f"    -> Report Headline: {lines[0] if lines else ''}")
                            print(f"    -> Sector/Industry: {lines[1] if len(lines) > 1 else ''}")
                    elif key == "web_research":
                        print(f"    -> Items Collected: {len(val)}")
                        for i, item in enumerate(val):
                            print(f"    -> Sub-item {i+1} status: {item.get('success')}")
                    elif key == "news_data":
                        print(f"    -> Status: {'Success' if val.get('success') else 'Fail'}")
                        if val.get("success"):
                            items = val.get("items", [])
                            print(f"    -> News articles parsed: {len(items)}")
                            for item in items[:2]:
                                print(f"       - [{item.get('relevance')}] {item.get('title')} ({item.get('source')})")
                    elif key == "draft":
                        print(f"    -> Memo Draft: {val[:120]}...")
                    elif key == "critic_verdict":
                        print(f"    -> Verdict: {val}")
                        
        print("\n" + "=" * 80)
        print("LANGGRAPH WORKFLOW EXECUTION COMPLETED")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Workflow execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
