from src.llm.schemas.registry import RelationshipRegistryEntry, SemanticRegistry


def add_relationships_to_registry(
    registry: SemanticRegistry,
    relationships: list[RelationshipRegistryEntry],
) -> SemanticRegistry:
    """
    Add discovered relationships to the semantic registry.

    Discovered relationships remain in their existing approval state.
    """

    registry.relationships.extend(relationships)

    return registry