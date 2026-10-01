from src.data.semantic.catalog.catalog import SemanticCatalogEntry
from src.query.retrieval.similarity import cosine_similarity
from src.embeddings.models.jina import embed_text
from src.llm.schemas.retrieval import SemanticCandidate


def retrieve_semantic_candidates(
    phrase: str,
    catalog: list[SemanticCatalogEntry],
    limit: int = 5,
) -> list[SemanticCandidate]:

    query_vector = embed_text(phrase)

    scored_candidates = []

    for entry in catalog:
        meaning_vector = embed_text(entry.approved_meaning)

        similarity = cosine_similarity(
            query_vector,
            meaning_vector,
        )

        scored_candidates.append(
            SemanticCandidate(
                semantic_id=entry.semantic_id,
                approved_meaning=entry.approved_meaning,
                similarity=similarity,
            )
        )

    scored_candidates.sort(
        key=lambda candidate: candidate.similarity,
        reverse=True,
    )

    return scored_candidates[:limit]