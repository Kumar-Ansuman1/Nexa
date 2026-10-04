from src.data.semantic.catalog.catalog import (
    SemanticCatalogEntry,
)
from src.query.retrieval.retriever import (
    retrieve_semantic_candidates,
)
from src.query.understanding.query_understanding import (
    understand_query,
)


def retrieve_query_candidates(
    query: str,
    catalog: list[SemanticCatalogEntry],
    stored_embeddings: dict[str, list[float]],
) -> dict:

    understanding = understand_query(query)

    results = {
        "metric": [],
        "dimensions": [],
        "time_phrase": understanding.time_phrase,
        "operation": understanding.operation,
    }

    if understanding.metric_phrase:
        results["metric"] = retrieve_semantic_candidates(
            phrase=understanding.metric_phrase,
            catalog=catalog,
            stored_embeddings=stored_embeddings,
        )

    for phrase in understanding.dimension_phrases:
        results["dimensions"].append(
            retrieve_semantic_candidates(
                phrase=phrase,
                catalog=catalog,
                stored_embeddings=stored_embeddings,
            )
        )

    return results