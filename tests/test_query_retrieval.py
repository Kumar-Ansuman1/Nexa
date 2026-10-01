from src.data.semantic.catalog import SemanticCatalogEntry
from src.data.semantic.query_retrieval import retrieve_query_candidates


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

query = "Show me revenue by subscription plan in March 2026."

results = retrieve_query_candidates(
    query=query,
    catalog=catalog,
)

print("\nMETRIC:")
for candidate in results["metric"]:
    print(candidate.model_dump())

print("\nDIMENSIONS:")
for candidates in results["dimensions"]:
    for candidate in candidates:
        print(candidate.model_dump())

print("\nTIME:")
print(results["time_phrase"])

print("\nOPERATION:")
print(results["operation"])