from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
)


def approve_column(
    column: ColumnRegistryEntry,
) -> ColumnRegistryEntry:

    if column.approval_status != ApprovalStatus.PENDING:
        raise ValueError(
            "Only pending columns can be approved."
        )

    column.approved_meaning = column.suggested_meaning
    column.approved_description = column.suggested_description
    column.approved_role = column.suggested_role
    column.approval_status = ApprovalStatus.APPROVED

    return column

def reject_column(
    column: ColumnRegistryEntry,
) -> ColumnRegistryEntry:

    if column.approval_status != ApprovalStatus.PENDING:
        raise ValueError(
            "Only pending columns can be rejected."
        )

    column.approval_status = ApprovalStatus.REJECTED

    return column

def edit_and_approve_column(
    column: ColumnRegistryEntry,
    approved_meaning: str,
    approved_description: str,
    approved_role: str,
) -> ColumnRegistryEntry:

    if column.approval_status != ApprovalStatus.PENDING:
        raise ValueError(
            "Only pending columns can be edited and approved."
        )

    column.approved_meaning = approved_meaning
    column.approved_description = approved_description
    column.approved_role = approved_role
    column.approval_status = ApprovalStatus.APPROVED

    return column