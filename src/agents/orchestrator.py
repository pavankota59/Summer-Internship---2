import logging

logger = logging.getLogger(__name__)

def run_orchestrator(company_query: str) -> dict:
    """
    Orchestrator node stub. Receives a query, defines a research plan,
    and coordinates other agents.
    """
    logger.info(f"Orchestrator starting process for query: {company_query}")
    # Plan template to be populated
    return {
        "query": company_query,
        "ticker": "N/A",
        "sub_questions": [
            {"question": "What is the company's financial health?", "agent": "financial_data"},
            {"question": "What are recent events or news?", "agent": "news_agent"},
            {"question": "Who are key competitors and what is their positioning?", "agent": "web_researcher"}
        ]
    }
