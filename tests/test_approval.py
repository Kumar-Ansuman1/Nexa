from src.data.semantic.registry.approval import approve_column
from src.data.semantic.registry.approval import reject_column
from src.data.semantic.registry.approval import edit_and_approve_column
from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
)


column = ColumnRegistryEntry(
    source_column="customer_id",
    suggested_meaning="customer_identifier",
    suggested_description="Unique identifier for a customer.",
    suggested_role="identifier",
    confidence=0.98,
    evidence=[
        "Column name contains customer_id",
        "Values are highly unique",
    ],
)


approved_column = approve_column(column)


print(approved_column.model_dump_json(indent=2))




rejected_column = reject_column(
    ColumnRegistryEntry(
        source_column="random_value",
        suggested_meaning="customer_identifier",
        suggested_description="Unique identifier for a customer.",
        suggested_role="identifier",
        confidence=0.55,
        evidence=[
            "Column contains unique values",
        ],
    )
)


print(rejected_column.model_dump_json(indent=2))




edited_column = edit_and_approve_column(
    ColumnRegistryEntry(
        source_column="value",
        suggested_meaning="transaction_amount",
        suggested_description="Monetary value of a transaction.",
        suggested_role="measure",
        confidence=0.80,
        evidence=[
            "Numeric column",
        ],
    ),
    approved_meaning="annual_contract_value",
    approved_description="Annual contract value associated with a customer.",
    approved_role="measure",
)


print(edited_column.model_dump_json(indent=2))