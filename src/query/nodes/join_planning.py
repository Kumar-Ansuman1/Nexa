from src.query.planning.join_planner import build_join_plan
from src.query.state import NexaQueryState


def build_join_plan_node(
    state: NexaQueryState,
) -> dict:
    """
    Build the join plan for the datasets required by the query.
    """

    query_plan = state["query_plan"]
    registry = state["registry"]

    join_plan = build_join_plan(
        query_plan=query_plan,
        registry=registry,
    )

    return {
        "join_plan": join_plan,
    }