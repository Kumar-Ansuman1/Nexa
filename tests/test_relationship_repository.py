from src.data.database.repositories.relationships import save_relationship
from src.llm.schemas.registry import (
    ApprovalStatus,
    RelationshipRegistryEntry,
)


relationship = RelationshipRegistryEntry(
    source_dataset="customers",
    source_column="customer_id",
    target_dataset="transactions",
    target_column="customer_id",
    relationship_type="one-to-many",
    confidence=0.99,
    evidence=[
        "Column names match",
        "Customer IDs appear in both datasets",
    ],
    approval_status=ApprovalStatus.PENDING,
)


relationship_id = save_relationship(
    relationship=relationship,
    source_dataset_id=1,
    source_column_id=1,
    target_dataset_id=2,
    target_column_id=2,
)

print(f"Saved relationship with ID: {relationship_id}")