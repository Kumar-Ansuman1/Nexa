from src.llm.schemas.registry import (
    ApprovalStatus,
    RelationshipRegistryEntry,
)
from src.llm.schemas.relationship import (
    RelationshipInterpretation,
)


def build_relationship_registry_entry(
    interpretation: RelationshipInterpretation,
) -> RelationshipRegistryEntry:

    return RelationshipRegistryEntry(
        source_dataset=interpretation.source_dataset,
        source_column=interpretation.source_column,
        target_dataset=interpretation.target_dataset,
        target_column=interpretation.target_column,
        relationship_type=interpretation.relationship_type,
        confidence=interpretation.confidence,
        evidence=interpretation.evidence,
        approval_status=ApprovalStatus.PENDING,
    )