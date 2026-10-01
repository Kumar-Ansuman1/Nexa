from src.data.semantic.query_resolver import resolve_query
from src.llm.schemas.semantic_query import SemanticQuery
from src.llm.schemas.query import QueryOperation
from src.llm.schemas.registry import (
    SemanticRegistry,
    DatasetRegistryEntry,
    ColumnRegistryEntry,
    ApprovalStatus,
)


registry = SemanticRegistry(
    datasets=[
        DatasetRegistryEntry(
            dataset_name="transactions",
            suggested_name="transactions",
            suggested_description="Transaction data",
            confidence=1.0,
            approval_status=ApprovalStatus.APPROVED,
            columns=[
                ColumnRegistryEntry(
                    semantic_id="sem_001",
                    source_column="amount",
                    suggested_meaning="Transaction amount",
                    suggested_description="Transaction monetary amount",
                    suggested_role="measure",
                    confidence=1.0,
                    evidence=[],
                    approved_meaning="Transaction amount",
                    approved_description="Transaction monetary amount",
                    approved_role="measure",
                    approval_status=ApprovalStatus.APPROVED,
                )
            ],
        ),
        DatasetRegistryEntry(
            dataset_name="customers",
            suggested_name="customers",
            suggested_description="Customer data",
            confidence=1.0,
            approval_status=ApprovalStatus.APPROVED,
            columns=[
                ColumnRegistryEntry(
                    semantic_id="sem_002",
                    source_column="plan",
                    suggested_meaning="Subscription plan",
                    suggested_description="Customer subscription plan",
                    suggested_role="category",
                    confidence=1.0,
                    evidence=[],
                    approved_meaning="Subscription plan",
                    approved_description="Customer subscription plan",
                    approved_role="category",
                    approval_status=ApprovalStatus.APPROVED,
                )
            ],
        ),
    ],
    relationships=[],
)


semantic_query = SemanticQuery(
    metric="sem_001",
    dimensions=["sem_002"],
    time_phrase="March 2026",
    operation=QueryOperation.SUM,
)


result = resolve_query(
    semantic_query=semantic_query,
    registry=registry,
)

print("\nResolved Query:")
print(result)