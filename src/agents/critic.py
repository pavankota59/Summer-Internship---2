import logging

logger = logging.getLogger(__name__)

def run_critic(draft: str, raw_inputs: dict) -> dict:
    """
    Critic Agent stub. Inspects draft for citation accuracy, missing risks, and contradictions.
    """
    logger.info("Critic Agent reviewing draft memo.")
    return {
        "status": "APPROVED",
        "feedback": "All requirements met. Draft looks solid.",
        "issues": []
    }
