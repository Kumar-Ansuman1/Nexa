from src.data.semantic.resolver import resolve_semantic_id
from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
    DatasetRegistryEntry,
    SemanticRegistry,
)


registry = SemanticRegistry(
    datasets=[
        DatasetRegistryEntry(
            dataset_name="customers",
            suggested_name="Customers",
            suggested_description="Customer information",
            confidence=0.95,
            approval_status=ApprovalStatus.APPROVED,
            columns=[
                ColumnRegistryEntry(
                    source_column="customer_id",
                    suggested_meaning="Customer identifier",
                    suggested_description="Unique identifier for a customer",
                    suggested_role="identifier",
                    confidence=0.99,
                    evidence=[],
                    approval_status=ApprovalStatus.APPROVED,
                ),
                ColumnRegistryEntry(
                    source_column="plan",
                    suggested_meaning="Subscription plan",
                    suggested_description="Customer subscription plan",
                    suggested_role="category",
                    confidence=0.95,
                    evidence=[],
                    approval_status=ApprovalStatus.PENDING,
                ),
            ],
        )
    ],
    relationships=[],
)


approved_id = registry.datasets[0].columns[0].semantic_id
pending_id = registry.datasets[0].columns[1].semantic_id


print(
    "Approved:",
    resolve_semantic_id(registry, approved_id),
)

print(
    "Pending:",
    resolve_semantic_id(registry, pending_id),
)

print(
    "Unknown:",
    resolve_semantic_id(registry, "sem_doesnotexist"),
)