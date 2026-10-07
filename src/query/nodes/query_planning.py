from src.query.planning.query_planner import build_query_plan
from src.query.state import NexaQueryState


def build_query_plan_node(
    state: NexaQueryState,
) -> dict:
    """
    Build the logical query plan from the resolved semantic query.
    """

    semantic_query = state["semantic_query"]
    resolved_query = state["resolved_query"]

    query_plan = build_query_plan(
        semantic_query=semantic_query,
        resolved_query=resolved_query,
    )

    return {
        "query_plan": query_plan,
    }