from src.data.semantic.registry.relationship_approval import (
    approve_relationship,
    reject_relationship,
    edit_and_approve_relationship,
)
from src.llm.schemas.registry import (
    ApprovalStatus,
    RelationshipRegistryEntry,
)


def create_test_relationship():
    return RelationshipRegistryEntry(
        source_dataset="customers",
        source_column="customer_id",
        target_dataset="transactions",
        target_column="customer_id",
        relationship_type="one_to_many",
        confidence=0.94,
        evidence=[
            "Source column is unique",
            "Target column contains repeated values",
        ],
        approval_status=ApprovalStatus.PENDING,
    )


def main():

    print("\n1. Approve")
    relationship = create_test_relationship()

    result = approve_relationship(relationship)

    print(result)
    print("Status:", result.approval_status)


    print("\n2. Reject")
    relationship = create_test_relationship()

    result = reject_relationship(relationship)

    print(result)
    print("Status:", result.approval_status)


    print("\n3. Edit + Approve")
    relationship = create_test_relationship()

    result = edit_and_approve_relationship(
        relationship=relationship,
        source_dataset="customers",
        source_column="customer_id",
        target_dataset="transactions",
        target_column="customer_id",
        relationship_type="one_to_many",
    )

    print(result)
    print("Status:", result.approval_status)


if __name__ == "__main__":
    main()