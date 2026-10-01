from src.query.resolution.jev_resolution import resolve_query_semantics
from src.data.semantic.catalog.catalog import SemanticCatalogEntry


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
        approved_meaning="Customer country",
    ),
]

query = "Show me revenue by subscription plan in March 2026."

result = resolve_query_semantics(
    query=query,
    catalog=catalog,
)

print("\nResolved Semantic Query:")
print(result.model_dump())