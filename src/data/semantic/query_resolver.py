from src.data.semantic.resolver import resolve_semantic_id
from src.llm.schemas.semantic_query import SemanticQuery


def resolve_query(
    semantic_query: SemanticQuery,
    registry,
) -> dict:

    metric = None

    if semantic_query.metric:
        metric = resolve_semantic_id(
            registry=registry,
            semantic_id=semantic_query.metric,
        )

    dimensions = []

    for semantic_id in semantic_query.dimensions:
        resolved = resolve_semantic_id(
            registry=registry,
            semantic_id=semantic_id,
        )

        if resolved:
            dimensions.append(resolved)

    return {
        "metric": metric,
        "dimensions": dimensions,
        "time_phrase": semantic_query.time_phrase,
        "operation": semantic_query.operation,
    }