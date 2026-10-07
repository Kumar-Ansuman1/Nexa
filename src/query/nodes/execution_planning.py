from src.query.planning.execution_planner import (
    build_execution_plan,
)
from src.query.state import NexaQueryState


def build_execution_plan_node(
    state: NexaQueryState,
) -> dict:
    """
    Build the execution plan from the query and join plans.
    """

    query_plan = state["query_plan"]
    join_plan = state["join_plan"]

    execution_plan = build_execution_plan(
        query_plan=query_plan,
        join_plan=join_plan,
    )

    return {
        "execution_plan": execution_plan,
    }