from src.data.database.repositories.registry import save_registry
from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
    DatasetRegistryEntry,
    SemanticRegistry,
)


registry = SemanticRegistry(
    datasets=[
        DatasetRegistryEntry(
            dataset_name="test_products",
            suggested_name="Products",
            suggested_description="Product records.",
            confidence=0.94,
            approval_status=ApprovalStatus.PENDING,
            columns=[
                ColumnRegistryEntry(
                    source_column="product_id",
                    suggested_meaning="product_identifier",
                    suggested_description="Unique product identifier.",
                    suggested_role="identifier",
                    confidence=0.99,
                    evidence=[
                        "Column name contains product_id",
                        "Values are unique",
                    ],
                    approval_status=ApprovalStatus.PENDING,
                ),
                ColumnRegistryEntry(
                    source_column="price",
                    suggested_meaning="product_price",
                    suggested_description="Price associated with a product.",
                    suggested_role="measure",
                    confidence=0.93,
                    evidence=[
                        "Numeric values",
                        "Column name contains price",
                    ],
                    approval_status=ApprovalStatus.PENDING,
                ),
            ],
        )
    ],
    relationships=[],
)


save_registry(registry)

print("Registry saved successfully.")