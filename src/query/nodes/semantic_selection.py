from src.query.state import NexaQueryState
from src.jev.selector import select_semantics
from src.llm.schemas.semantic_query import SemanticQuery


def select_semantics_node(
    state: NexaQueryState,
) -> dict:
    """
    Use Data JEV to select the semantic metric and dimension
    from the candidates retrieved for the user's query.
    """

    query = state["user_query"]
    candidates = state["candidates"]

    metric_candidates = candidates["metric"]
    dimension_candidates = candidates["dimensions"]

    if not metric_candidates:
        raise ValueError(
            "No metric candidates were retrieved for the query."
        )

    if not dimension_candidates:
        raise ValueError(
            "No dimension candidates were retrieved for the query."
        )

    selection = select_semantics(
        query=query,
        metric_candidates=metric_candidates,
        dimension_candidates=dimension_candidates[0],
    )

    semantic_query = SemanticQuery(
        metric=selection.metric,
        dimensions=selection.dimensions,
        time_phrase=candidates["time_phrase"],
        operation=candidates["operation"],
    )

    return {
        "semantic_query": semantic_query,
    }