from src.data.database.repositories.registry import save_registry
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
            dataset_name="customers_test",
            suggested_name="Customers",
            suggested_description="Customer records.",
            confidence=0.96,
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
            dataset_name="transactions_test",
            suggested_name="Transactions",
            suggested_description="Transaction records.",
            confidence=0.95,
            approval_status=ApprovalStatus.PENDING,
            columns=[
                ColumnRegistryEntry(
                    source_column="customer_id",
                    suggested_meaning="customer_identifier",
                    suggested_description="Customer associated with transaction.",
                    suggested_role="foreign_key",
                    confidence=0.98,
                    evidence=["Matches customers.customer_id"],
                    approval_status=ApprovalStatus.PENDING,
                )
            ],
        ),
    ],
    relationships=[
        RelationshipRegistryEntry(
            source_dataset="customers_test",
            source_column="customer_id",
            target_dataset="transactions_test",
            target_column="customer_id",
            relationship_type="one-to-many",
            confidence=0.99,
            evidence=["Matching customer identifiers"],
            approval_status=ApprovalStatus.PENDING,
        )
    ],
)


save_registry(registry)

print("Full registry saved successfully.")