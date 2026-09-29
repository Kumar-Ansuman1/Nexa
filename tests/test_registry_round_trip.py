from src.data.database.repositories.registry import load_registry, save_registry

from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
    DatasetRegistryEntry,
    RelationshipRegistryEntry,
    SemanticRegistry,
)


registry = SemanticRegistry(
    datasets=[
        DatasetRegistryEntry(
            dataset_name="round_trip_customers",
            suggested_name="Customers",
            suggested_description="Customer dataset.",
            confidence=0.97,
            approval_status=ApprovalStatus.PENDING,
            columns=[
                ColumnRegistryEntry(
                    source_column="customer_id",
                    suggested_meaning="customer_identifier",
                    suggested_description="Unique customer identifier.",
                    suggested_role="identifier",
                    confidence=0.99,
                    evidence=["Unique values"],
                    approval_status=ApprovalStatus.PENDING,
                )
            ],
        ),
        DatasetRegistryEntry(
            dataset_name="round_trip_transactions",
            suggested_name="Transactions",
            suggested_description="Transaction dataset.",
            confidence=0.96,
            approval_status=ApprovalStatus.PENDING,
            columns=[
                ColumnRegistryEntry(
                    source_column="customer_id",
                    suggested_meaning="customer_identifier",
                    suggested_description="Customer associated with the transaction.",
                    suggested_role="foreign_key",
                    confidence=0.98,
                    evidence=["Repeated values"],
                    approval_status=ApprovalStatus.PENDING,
                )
            ],
        ),
    ],
    relationships=[
        RelationshipRegistryEntry(
            source_dataset="round_trip_customers",
            source_column="customer_id",
            target_dataset="round_trip_transactions",
            target_column="customer_id",
            relationship_type="one_to_many",
            confidence=0.94,
            evidence=[
                "Customer IDs are unique in the customers dataset.",
                "Customer IDs repeat across transactions.",
            ],
            approval_status=ApprovalStatus.APPROVED,
        )
    ],
)


# Save registry
save_registry(registry)

# Load registry
loaded_registry = load_registry()

# Print loaded registry
print(loaded_registry.model_dump_json(indent=2))