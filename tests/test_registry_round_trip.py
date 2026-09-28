from src.data.database.repositories.registry import (
    load_registry,
    save_registry,
)
from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
    DatasetRegistryEntry,
    SemanticRegistry,
)


registry = SemanticRegistry(
    datasets=[
        DatasetRegistryEntry(
            dataset_name="round_trip_test",
            suggested_name="Round Trip Test",
            suggested_description="Testing registry persistence.",
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
        )
    ],
    relationships=[],
)


save_registry(registry)

loaded_registry = load_registry()

print(loaded_registry.model_dump_json(indent=2))