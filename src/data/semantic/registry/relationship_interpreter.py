from src.llm.models.groq import GroqModel
from src.llm.prompts.relationship_interpretation import (
    build_relationship_interpretation_prompt,
)
from src.llm.schemas.relationship import (
    RelationshipCandidate,
    RelationshipInterpretation,
)


def interpret_relationship(
    candidate: RelationshipCandidate,
) -> RelationshipInterpretation:

    prompt = build_relationship_interpretation_prompt(
        candidate
    )

    llm = GroqModel()

    return llm.generate_structured(
        prompt=prompt,
        response_model=RelationshipInterpretation,
    )