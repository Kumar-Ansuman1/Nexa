from src.data.database.repositories.datasets import save_dataset
from src.data.database.repositories.columns import save_column
from src.data.database.repositories.columns import get_columns
from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
    DatasetRegistryEntry,
)


dataset = DatasetRegistryEntry(
    dataset_name="test_customers",
    suggested_name="Test Customers",
    suggested_description="Test customer dataset.",
    confidence=0.95,
    approval_status=ApprovalStatus.PENDING,
    columns=[],
)

dataset_id = save_dataset(dataset)


column = ColumnRegistryEntry(
    source_column="customer_id",
    suggested_meaning="customer_identifier",
    suggested_description="Unique customer identifier.",
    suggested_role="identifier",
    confidence=0.98,
    evidence=[
        "Column name contains customer_id",
        "Values are highly unique",
    ],
    approval_status=ApprovalStatus.PENDING,
)

save_column(
    column=column,
    dataset_id=dataset_id,
)


columns = get_columns(dataset_id)

for column in columns:
    print(column.model_dump_json(indent=2))