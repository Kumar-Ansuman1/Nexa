from src.data.semantic.relationship_approval import approve_relationship
from src.data.semantic.relationship_registry_builder import (
    build_relationship_registry_entry,
)
from src.llm.schemas.relationship import RelationshipInterpretation


def main():

    interpretation = RelationshipInterpretation(
        source_dataset="customers",
        source_column="customer_id",
        target_dataset="transactions",
        target_column="customer_id",
        relationship_type="one_to_many",
        confidence=0.94,
        evidence=[
            "Customer ID is unique in customers",
            "Customer ID repeats in transactions",
            "Values overlap completely",
        ],
    )

    relationship = build_relationship_registry_entry(
        interpretation
    )

    print("\nBefore approval:")
    print(relationship)

    relationship = approve_relationship(
        relationship
    )

    print("\nAfter approval:")
    print(relationship)


if __name__ == "__main__":
    main()