from src.llm.schemas.retrieval import SemanticCandidate
from src.jev.selector import select_semantics


metric_candidates = [
    SemanticCandidate(
        semantic_id="sem_001",
        approved_meaning="Transaction amount",
        similarity=0.60,
    ),
    SemanticCandidate(
        semantic_id="sem_014",
        approved_meaning="Subscription revenue",
        similarity=0.58,
    ),
    SemanticCandidate(
        semantic_id="sem_027",
        approved_meaning="Invoice total",
        similarity=0.55,
    ),
]

dimension_candidates = [
    SemanticCandidate(
        semantic_id="sem_002",
        approved_meaning="Subscription plan",
        similarity=0.98,
    ),
    SemanticCandidate(
        semantic_id="sem_021",
        approved_meaning="Current customer plan",
        similarity=0.82,
    ),
]

query = "Show me revenue by subscription plan in March 2026."

result = select_semantics(
    query=query,
    metric_candidates=metric_candidates,
    dimension_candidates=dimension_candidates,
)

print(result.model_dump())