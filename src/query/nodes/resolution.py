from src.query.resolution.resolver import resolve_semantic_id
from src.query.state import NexaQueryState


def resolve_semantics_node(
    state: NexaQueryState,
) -> dict:
    """
    Resolve the semantic IDs selected by Data JEV into
    physical dataset and source-column references.
    """

    semantic_query = state["semantic_query"]
    registry = state["registry"]

    metric = None

    if semantic_query.metric:
        metric = resolve_semantic_id(
            registry=registry,
            semantic_id=semantic_query.metric,
        )

        if metric is None:
            raise ValueError(
                f"Unable to resolve metric semantic ID: "
                f"{semantic_query.metric}"
            )

    dimensions = []

    for semantic_id in semantic_query.dimensions:
        resolved = resolve_semantic_id(
            registry=registry,
            semantic_id=semantic_id,
        )

        if resolved is None:
            raise ValueError(
                f"Unable to resolve dimension semantic ID: "
                f"{semantic_id}"
            )

        dimensions.append(resolved)

    resolved_query = {
        "metric": metric,
        "dimensions": dimensions,
        "time_phrase": semantic_query.time_phrase,
        "operation": semantic_query.operation,
    }

    return {
        "resolved_query": resolved_query,
    }