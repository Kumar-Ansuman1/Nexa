from src.llm.schemas.registry import (
    ApprovalStatus,
    SemanticRegistry,
)


def resolve_semantic_id(
    registry: SemanticRegistry,
    semantic_id: str,
) -> tuple[str, str] | None:

    for dataset in registry.datasets:
        for column in dataset.columns:

            if (
                column.semantic_id == semantic_id
                and column.approval_status == ApprovalStatus.APPROVED
            ):
                return dataset.dataset_name, column.source_column

    return None