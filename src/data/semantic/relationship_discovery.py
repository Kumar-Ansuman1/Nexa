from src.data.semantic.relationship_candidates import generate_relationship_candidates
from src.data.semantic.relationship_interpreter import interpret_relationship
from src.data.semantic.relationship_registry_builder import (
    build_relationship_registry_entry,
)
from src.llm.schemas.registry import RelationshipRegistryEntry, SemanticRegistry


def discover_relationships(
    datasets: dict,
    registry: SemanticRegistry,
) -> list[RelationshipRegistryEntry]:
    """
    Discover meaningful relationships between datasets.

    Flow:
    1. Generate deterministic relationship candidates.
    2. Ask the LLM to interpret each candidate.
    3. Convert interpretations into pending registry entries.

    Relationships are NOT automatically approved.
    """

    candidates = generate_relationship_candidates(
        datasets=datasets,
        registry=registry,
    )

    relationships = []

    for candidate in candidates:
        interpretation = interpret_relationship(candidate)

        if interpretation.relationship_type == "no_relationship":
            continue

        registry_entry = build_relationship_registry_entry(
            interpretation
        )

        relationships.append(registry_entry)

    return relationships