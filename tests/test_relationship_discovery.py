import pandas as pd

from src.data.semantic.relationship_discovery import discover_relationships
from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
    DatasetRegistryEntry,
    SemanticRegistry,
)


customers = pd.DataFrame(
    {
        "customer_id": [1, 2, 3, 4, 5],
        "name": ["A", "B", "C", "D", "E"],
    }
)

transactions = pd.DataFrame(
    {
        "transaction_id": [101, 102, 103, 104, 105, 106],
        "customer_id": [1, 1, 2, 3, 3, 5],
        "amount": [100, 200, 150, 300, 250, 500],
    }
)


registry = SemanticRegistry(
    datasets=[
        DatasetRegistryEntry(
            dataset_name="customers",
            suggested_name="Customers",
            suggested_description="Customer dataset.",
            confidence=0.99,
            approval_status=ApprovalStatus.APPROVED,
            columns=[
                ColumnRegistryEntry(
                    source_column="customer_id",
                    suggested_meaning="customer_identifier",
                    suggested_description="Unique customer identifier.",
                    suggested_role="identifier",
                    confidence=0.99,
                    evidence=["Unique values"],
                    approved_meaning="customer_identifier",
                    approved_description="Unique customer identifier.",
                    approved_role="identifier",
                    approval_status=ApprovalStatus.APPROVED,
                ),
                ColumnRegistryEntry(
                    source_column="name",
                    suggested_meaning="customer_name",
                    suggested_description="Customer name.",
                    suggested_role="attribute",
                    confidence=0.99,
                    evidence=["Text values"],
                    approved_meaning="customer_name",
                    approved_description="Customer name.",
                    approved_role="attribute",
                    approval_status=ApprovalStatus.APPROVED,
                ),
            ],
        ),
        DatasetRegistryEntry(
            dataset_name="transactions",
            suggested_name="Transactions",
            suggested_description="Transaction dataset.",
            confidence=0.99,
            approval_status=ApprovalStatus.APPROVED,
            columns=[
                ColumnRegistryEntry(
                    source_column="transaction_id",
                    suggested_meaning="transaction_identifier",
                    suggested_description="Unique transaction identifier.",
                    suggested_role="identifier",
                    confidence=0.99,
                    evidence=["Unique values"],
                    approved_meaning="transaction_identifier",
                    approved_description="Unique transaction identifier.",
                    approved_role="identifier",
                    approval_status=ApprovalStatus.APPROVED,
                ),
                ColumnRegistryEntry(
                    source_column="customer_id",
                    suggested_meaning="customer_identifier",
                    suggested_description="Customer associated with transaction.",
                    suggested_role="foreign_key",
                    confidence=0.99,
                    evidence=["Repeated customer IDs"],
                    approved_meaning="customer_identifier",
                    approved_description="Customer associated with transaction.",
                    approved_role="foreign_key",
                    approval_status=ApprovalStatus.APPROVED,
                ),
            ],
        ),
    ],
    relationships=[],
)


datasets = {
    "customers": customers,
    "transactions": transactions,
}


relationships = discover_relationships(
    datasets=datasets,
    registry=registry,
)


print("\nDiscovered relationships:\n")

for relationship in relationships:
    print(
        f"{relationship.source_dataset}."
        f"{relationship.source_column}"
        f" -> "
        f"{relationship.target_dataset}."
        f"{relationship.target_column}"
    )

    print(f"Type: {relationship.relationship_type}")
    print(f"Confidence: {relationship.confidence}")
    print(f"Status: {relationship.approval_status}")
    print(f"Evidence: {relationship.evidence}")
    print()