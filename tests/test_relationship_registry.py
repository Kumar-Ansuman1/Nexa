from src.data.semantic.relationship_registry import (
    add_relationships_to_registry,
)
from src.llm.schemas.registry import (
    ApprovalStatus,
    RelationshipRegistryEntry,
    SemanticRegistry,
)


registry = SemanticRegistry(
    datasets=[],
    relationships=[],
)


relationship = RelationshipRegistryEntry(
    source_dataset="customers",
    source_column="customer_id",
    target_dataset="transactions",
    target_column="customer_id",
    relationship_type="one_to_many",
    confidence=0.94,
    evidence=[
        "Customer IDs are unique in customers.",
        "Customer IDs repeat in transactions.",
    ],
    approval_status=ApprovalStatus.PENDING,
)


updated_registry = add_relationships_to_registry(
    registry=registry,
    relationships=[relationship],
)


print("Relationships in registry:", len(updated_registry.relationships))

print(
    updated_registry.relationships[0].source_dataset,
    updated_registry.relationships[0].source_column,
    "->",
    updated_registry.relationships[0].target_dataset,
    updated_registry.relationships[0].target_column,
)

print(
    "Status:",
    updated_registry.relationships[0].approval_status,
)