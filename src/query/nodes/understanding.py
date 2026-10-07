from src.query.state import NexaQueryState
from src.query.understanding.query_understanding import (
    understand_query,
)


def understand_query_node(
    state: NexaQueryState,
) -> dict:
    """
    Run query understanding for the user's natural-language query.

    This node extracts the structured query intent required by
    downstream semantic retrieval.
    """

    query = state["user_query"]

    understanding = understand_query(
        query=query,
    )

    return {
        "understanding": understanding,
    }