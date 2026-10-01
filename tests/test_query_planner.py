from src.query.planning.query_planner import build_query_plan
from src.llm.schemas.semantic_query import SemanticQuery
from src.llm.schemas.query import QueryOperation


semantic_query = SemanticQuery(
    metric="sem_001",
    dimensions=["sem_002"],
    time_phrase="March 2026",
    operation=QueryOperation.SUM,
)


resolved_query = {
    "metric": ("transactions", "amount"),
    "dimensions": [
        ("customers", "plan"),
    ],
    "time_phrase": "March 2026",
    "operation": QueryOperation.SUM,
}


result = build_query_plan(
    semantic_query=semantic_query,
    resolved_query=resolved_query,
)

print("\nQuery Plan:")
print(result.model_dump())