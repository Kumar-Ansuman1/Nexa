from src.data.database.repositories.columns import save_column
from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
)


column = ColumnRegistryEntry(
    source_column="customer_id",
    suggested_meaning="customer_identifier",
    suggested_description="Unique identifier for a customer.",
    suggested_role="identifier",
    confidence=0.98,
    evidence=[
        "Column name contains customer_id",
        "Values are highly unique",
    ],
    approval_status=ApprovalStatus.PENDING,
)


column_id = save_column(
    column=column,
    dataset_id=1,
)

print(f"Saved column with ID: {column_id}")