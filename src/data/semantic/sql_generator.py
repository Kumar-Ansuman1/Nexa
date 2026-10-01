from src.llm.models.groq import GroqModel
from src.llm.prompts.sql_generation import build_sql_generation_prompt
from src.llm.schemas.sql_generation import SQLQuery


def generate_sql(
    execution_plan: dict,
    database_schema: str,
) -> SQLQuery:

    prompt = build_sql_generation_prompt(
        execution_plan=execution_plan,
        database_schema=database_schema,
    )

    llm = GroqModel()

    return llm.generate_structured(
        prompt=prompt,
        response_model=SQLQuery,
    )