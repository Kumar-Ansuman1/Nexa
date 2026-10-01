from src.llm.schemas.registry import ApprovalStatus, RelationshipRegistryEntry


def approve_relationship(
    relationship: RelationshipRegistryEntry,
) -> RelationshipRegistryEntry:

    if relationship.approval_status != ApprovalStatus.PENDING:
        raise ValueError(
            "Only pending relationships can be approved."
        )

    relationship.approval_status = ApprovalStatus.APPROVED

    return relationship

def reject_relationship(
    relationship: RelationshipRegistryEntry,
) -> RelationshipRegistryEntry:

    if relationship.approval_status != ApprovalStatus.PENDING:
        raise ValueError(
            "Only pending relationships can be rejected."
        )

    relationship.approval_status = ApprovalStatus.REJECTED

    return relationship

def edit_and_approve_relationship(
    relationship: RelationshipRegistryEntry,
    source_dataset: str,
    source_column: str,
    target_dataset: str,
    target_column: str,
    relationship_type: str,
) -> RelationshipRegistryEntry:

    if relationship.approval_status != ApprovalStatus.PENDING:
        raise ValueError(
            "Only pending relationships can be edited and approved."
        )

    relationship.source_dataset = source_dataset
    relationship.source_column = source_column
    relationship.target_dataset = target_dataset
    relationship.target_column = target_column
    relationship.relationship_type = relationship_type

    relationship.approval_status = ApprovalStatus.APPROVED

    return relationship