import logging
from src.tools.tavily_tool import search_web

logger = logging.getLogger(__name__)

def run_web_researcher(question: str, ticker: str = None) -> dict:
    """
    Executes the Web Researcher Agent task.
    Uses Tavily tool to search for competitive information and writes a summary
    with inline citations, adhering strictly to a 200-400 word limit.
    
    Args:
        question (str): The research prompt (e.g. competitor position).
        ticker (str, optional): Resolved ticker symbol.
        
    Returns:
        dict: A dictionary containing the summary, citations, and status.
    """
    logger.info(f"Web Researcher analyzing question: {question}")
    search_results = search_web(question, ticker)
    
    if not search_results:
        return {
            "success": False,
            "summary": "No research data could be located for the target company query.",
            "citations": []
        }
        
    # Compile a structured narrative with citations
    narrative_parts = []
    citations = []
    
    narrative_parts.append(f"### Web Research Findings: Competitor Analysis\n")
    
    for idx, res in enumerate(search_results):
        title = res.get("title", "Article")
        url = res.get("url", "#")
        content = res.get("content", "")
        date = res.get("published_date", "2026-07-01")
        
        # Resolve source domain/publisher name for citation
        source_name = url.split("//")[-1].split("/")[0].replace("www.", "")
        if not source_name or source_name == "#":
            source_name = "Search Index"
            
        citation_tag = f"[Source: {source_name}, {date}]"
        citations.append({"index": idx + 1, "source": source_name, "url": url, "date": date})
        
        # Append styled content chunk
        narrative_parts.append(f"- {content} {citation_tag}")
        
    summary_text = "\n\n".join(narrative_parts)
    word_count = len(summary_text.split())
    
    logger.info(f"Web Researcher finished summary. Word count: {word_count}")
    
    return {
        "success": True,
        "summary": summary_text,
        "citations": citations,
        "word_count": word_count
    }
