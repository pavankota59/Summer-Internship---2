import logging
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

# Import agent nodes
from src.agents.orchestrator import run_orchestrator
from src.agents.financial_data import run_financial_data_agent
from src.agents.web_researcher import run_web_researcher
from src.agents.news_agent import run_news_agent
from src.agents.writer import run_writer
from src.agents.critic import run_critic

logger = logging.getLogger(__name__)

# Define state structure
class AgentState(TypedDict):
    query: str
    ticker: str
    financial_data: Dict[str, Any]
    web_research: List[Dict[str, Any]]
    news_data: Dict[str, Any]
    draft: str
    critic_feedback: List[str]
    critic_verdict: str  # APPROVED or REVISE
    loop_count: int
    published: bool

def orchestrator_node(state: AgentState) -> Dict[str, Any]:
    logger.info("Executing Orchestrator Node...")
    plan = run_orchestrator(state["query"])
    # Stub resolves ticker from query for demonstration
    ticker = "RELIANCE.NS" if "reliance" in state["query"].lower() else "TCS.NS"
    return {"ticker": ticker}

def financial_data_node(state: AgentState) -> Dict[str, Any]:
    logger.info("Executing Financial Data Agent Node...")
    result = run_financial_data_agent(state["ticker"])
    return {"financial_data": result}

def web_research_node(state: AgentState) -> Dict[str, Any]:
    logger.info("Executing Web Researcher Agent Node...")
    result = run_web_researcher(f"Perform market position analysis for {state['ticker']}")
    return {"web_research": [result]}

def news_node(state: AgentState) -> Dict[str, Any]:
    logger.info("Executing News Agent Node...")
    result = run_news_agent(state["ticker"])
    return {"news_data": result}

def writer_node(state: AgentState) -> Dict[str, Any]:
    logger.info("Executing Writer Agent Node...")
    inputs = {
        "financial_data": state.get("financial_data"),
        "web_research": state.get("web_research"),
        "news_data": state.get("news_data")
    }
    result = run_writer(inputs)
    return {"draft": result["draft"]}

def critic_node(state: AgentState) -> Dict[str, Any]:
    logger.info("Executing Critic Agent Node...")
    inputs = {
        "financial_data": state.get("financial_data"),
        "web_research": state.get("web_research"),
        "news_data": state.get("news_data")
    }
    result = run_critic(state["draft"], inputs)
    return {
        "critic_verdict": result["status"],
        "critic_feedback": state.get("critic_feedback", []) + [result["feedback"]],
        "loop_count": state.get("loop_count", 0) + 1
    }

def critic_routing_logic(state: AgentState) -> str:
    # Router logic to redirect back to writer or approve
    if state["critic_verdict"] == "APPROVED" or state.get("loop_count", 0) >= 2:
        return "approve"
    return "revise"

# Build State Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("financial_data_agent", financial_data_node)
workflow.add_node("web_research_agent", web_research_node)
workflow.add_node("news_agent", news_node)
workflow.add_node("writer", writer_node)
workflow.add_node("critic", critic_node)

# Wire the graph edges
workflow.set_entry_point("orchestrator")

workflow.add_edge("orchestrator", "financial_data_agent")
workflow.add_edge("orchestrator", "web_research_agent")
workflow.add_edge("orchestrator", "news_agent")

workflow.add_edge("financial_data_agent", "writer")
workflow.add_edge("web_research_agent", "writer")
workflow.add_edge("news_agent", "writer")

workflow.add_edge("writer", "critic")

workflow.add_conditional_edges(
    "critic",
    critic_routing_logic,
    {
        "revise": "writer",
        "approve": END
    }
)

app_graph = workflow.compile()
