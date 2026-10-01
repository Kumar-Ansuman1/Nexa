from src.data.semantic.catalog import build_semantic_catalog
from src.data.semantic.resolver import resolve_semantic_id
from src.jev.selector import select_query_semantics
from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
    DatasetRegistryEntry,
    SemanticRegistry,
)


registry = SemanticRegistry(
    datasets=[
        DatasetRegistryEntry(
            dataset_name="transactions",
            suggested_name="Transactions",
            suggested_description="Customer transaction records",
            confidence=0.98,
            approval_status=ApprovalStatus.APPROVED,
            columns=[
                ColumnRegistryEntry(
                    source_column="amount",
                    suggested_meaning="Transaction amount",
                    suggested_description="Monetary value of a transaction",
                    suggested_role="measure",
                    confidence=0.99,
                    evidence=[],
                    approved_meaning="Transaction amount",
                    approved_description="Monetary value of a transaction",
                    approved_role="measure",
                    approval_status=ApprovalStatus.APPROVED,
                ),
                ColumnRegistryEntry(
                    source_column="date",
                    suggested_meaning="Transaction date",
                    suggested_description="Date when the transaction occurred",
                    suggested_role="timestamp",
                    confidence=0.99,
                    evidence=[],
                    approved_meaning="Transaction date",
                    approved_description="Date when the transaction occurred",
                    approved_role="timestamp",
                    approval_status=ApprovalStatus.APPROVED,
                ),
            ],
        ),
        DatasetRegistryEntry(
            dataset_name="customers",
            suggested_name="Customers",
            suggested_description="Customer information",
            confidence=0.98,
            approval_status=ApprovalStatus.APPROVED,
            columns=[
                ColumnRegistryEntry(
                    source_column="plan",
                    suggested_meaning="Subscription plan",
                    suggested_description="Customer subscription plan",
                    suggested_role="category",
                    confidence=0.98,
                    evidence=[],
                    approved_meaning="Subscription plan",
                    approved_description="Customer subscription plan",
                    approved_role="category",
                    approval_status=ApprovalStatus.APPROVED,
                ),
            ],
        ),
    ],
    relationships=[],
)


query = "Show revenue by subscription plan in March 2026."


# 1. Build approved semantic choices
catalog = build_semantic_catalog(registry)

print("Catalog:")
for entry in catalog:
    print(entry.model_dump())


# 2. Let Jev select the relevant semantic IDs
selection = select_query_semantics(
    query=query,
    catalog=catalog,
)

print("\nJev selection:")
print(selection.model_dump())


# 3. Resolve Jev's semantic IDs to real source columns
metric = resolve_semantic_id(
    registry,
    selection.metric,
)

dimension = resolve_semantic_id(
    registry,
    selection.dimensions[0],
)

time_column = resolve_semantic_id(
    registry,
    selection.time_semantic_id,
)

print("\nResolved columns:")
print("Metric:", metric)
print("Dimension:", dimension)
print("Time:", time_column)