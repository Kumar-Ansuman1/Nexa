from src.query.retrieval.query_retrieval import retrieve_query_candidates
from src.jev.selector import select_semantics
from src.llm.schemas.semantic_query import SemanticQuery


def resolve_query_semantics(
    query: str,
    catalog,
) -> SemanticQuery:

    candidates = retrieve_query_candidates(
        query=query,
        catalog=catalog,
    )

    selection = select_semantics(
        query=query,
        metric_candidates=candidates["metric"],
        dimension_candidates=candidates["dimensions"][0],
    )

    return SemanticQuery(
        metric=selection.metric,
        dimensions=selection.dimensions,
        time_phrase=candidates["time_phrase"],
        operation=candidates["operation"],
    )