from src.query.planning.join_planner import build_join_plan
from src.llm.schemas.query_plan import QueryPlan, ResolvedColumn
from src.llm.schemas.query import QueryOperation
from src.llm.schemas.registry import (
    SemanticRegistry,
    RelationshipRegistryEntry,
    ApprovalStatus,
)


query_plan = QueryPlan(
    metric=ResolvedColumn(
        dataset="transactions",
        column="amount",
    ),
    dimensions=[
        ResolvedColumn(
            dataset="customers",
            column="plan",
        )
    ],
    operation=QueryOperation.SUM,
    time_phrase="March 2026",
    required_datasets=[
        "transactions",
        "customers",
    ],
)


registry = SemanticRegistry(
    datasets=[],
    relationships=[
        RelationshipRegistryEntry(
            source_dataset="customers",
            source_column="customer_id",
            target_dataset="transactions",
            target_column="customer_id",
            relationship_type="one_to_many",
            confidence=0.95,
            evidence=["customer_id values overlap"],
            approval_status=ApprovalStatus.APPROVED,
        )
    ],
)


result = build_join_plan(
    query_plan=query_plan,
    registry=registry,
)

print("\nJoin Plan:")
print(result.model_dump())