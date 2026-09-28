from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
    DatasetRegistryEntry,
    RelationshipRegistryEntry,
    SemanticRegistry,
)


column = ColumnRegistryEntry(
    source_column="customer_id",
    suggested_meaning="customer_identifier",
    suggested_description="Unique identifier for a customer.",
    suggested_role="identifier",
    confidence=0.98,
    evidence=[
        "Column contains unique values",
        "Column name contains customer_id",
    ],
)


dataset = DatasetRegistryEntry(
    dataset_name="customers",
    suggested_name="Customers",
    suggested_description="Records representing company customers.",
    confidence=0.96,
    columns=[column],
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
)


registry = SemanticRegistry(
    datasets=[dataset],
    relationships=[relationship],
)


print(registry.model_dump_json(indent=2))