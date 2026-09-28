from src.data.semantic.registry_builder import build_registry_entry
from src.llm.schemas.semantic import (
    DatasetInterpretation,
    SemanticMapping,
    SemanticSuggestion,
)


mapping = SemanticMapping(
    dataset=DatasetInterpretation(
        suggested_name="Customers",
        description="Records representing company customers.",
        confidence=0.96,
    ),
    columns=[
        SemanticSuggestion(
            source_column="customer_id",
            suggested_meaning="customer_identifier",
            description="Unique identifier for a customer.",
            role="identifier",
            confidence=0.98,
            evidence=[
                "Column name contains customer_id",
                "Values are highly unique",
            ],
        )
    ],
)


registry_entry = build_registry_entry(
    mapping=mapping,
    dataset_name="customers",
)


print(registry_entry.model_dump_json(indent=2))