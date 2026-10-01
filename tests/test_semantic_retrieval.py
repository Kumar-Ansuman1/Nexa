from src.data.semantic.catalog.catalog import SemanticCatalogEntry
from src.query.retrieval.retriever import retrieve_semantic_candidates

catalog = [
    SemanticCatalogEntry(
        semantic_id="sem_001",
        approved_meaning="Transaction amount",
    ),
    SemanticCatalogEntry(
        semantic_id="sem_002",
        approved_meaning="Subscription plan",
    ),
    SemanticCatalogEntry(
        semantic_id="sem_003",
        approved_meaning="Transaction date",
    ),
    SemanticCatalogEntry(
        semantic_id="sem_004",
        approved_meaning="Customer country",
    ),
]

results = retrieve_semantic_candidates(
    phrase="revenue",
    catalog=catalog,
    limit=3,
)

for result in results:
    print(result.model_dump())