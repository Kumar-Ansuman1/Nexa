from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
    DatasetRegistryEntry,
)
from src.llm.schemas.semantic import SemanticMapping


def build_registry_entry(
    mapping: SemanticMapping,
    dataset_name: str,
) -> DatasetRegistryEntry:

    columns = []

    for suggestion in mapping.columns:
        column = ColumnRegistryEntry(
            source_column=suggestion.source_column,
            suggested_meaning=suggestion.suggested_meaning,
            suggested_description=suggestion.description,
            suggested_role=suggestion.role,
            confidence=suggestion.confidence,
            evidence=suggestion.evidence,
            approval_status=ApprovalStatus.PENDING,
        )

        columns.append(column)

    return DatasetRegistryEntry(
        dataset_name=dataset_name,
        suggested_name=mapping.dataset.suggested_name,
        suggested_description=mapping.dataset.description,
        confidence=mapping.dataset.confidence,
        approval_status=ApprovalStatus.PENDING,
        columns=columns,
    )