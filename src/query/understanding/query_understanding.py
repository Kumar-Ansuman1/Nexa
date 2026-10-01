from src.llm.models.groq import GroqModel
from src.llm.prompts.query_understanding import (
    build_query_understanding_prompt,
)
from src.llm.schemas.query_understanding import QueryUnderstanding


def understand_query(query: str) -> QueryUnderstanding:
    prompt = build_query_understanding_prompt(query)

    llm = GroqModel()

    return llm.generate_structured(
        prompt=prompt,
        response_model=QueryUnderstanding,
    )