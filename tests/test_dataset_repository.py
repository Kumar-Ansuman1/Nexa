from src.data.database.repositories.datasets import save_dataset
from src.llm.schemas.registry import (
    ApprovalStatus,
    DatasetRegistryEntry,
)


dataset = DatasetRegistryEntry(
    dataset_name="customers",
    suggested_name="Customers",
    suggested_description="Records representing company customers.",
    confidence=0.96,
    approval_status=ApprovalStatus.PENDING,
    columns=[],
)


dataset_id = save_dataset(dataset)

print(f"Saved dataset with ID: {dataset_id}")