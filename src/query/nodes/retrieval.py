from src.query.state import NexaQueryState
from src.query.retrieval.retriever import (
    retrieve_semantic_candidates,
)


def retrieve_semantic_candidates_node(
    state: NexaQueryState,
) -> dict:
    """
    Retrieve semantic candidates using the query understanding
    already stored in the workflow state.
    """

    understanding = state["understanding"]

    catalog = state["catalog"]
    stored_embeddings = state["stored_embeddings"]

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

    return {
        "candidates": results,
    }