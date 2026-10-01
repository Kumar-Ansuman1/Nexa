from src.llm.models.groq import GroqModel
from src.llm.prompts.semantic_interpretation import (
    build_semantic_interpretation_prompt,
)
from src.llm.schemas.semantic import SemanticMapping


def interpret_dataset(profile: dict) -> SemanticMapping:
    prompt = build_semantic_interpretation_prompt(profile)

    llm = GroqModel()

    return llm.generate_structured(
        prompt=prompt,
        response_model=SemanticMapping,
    )