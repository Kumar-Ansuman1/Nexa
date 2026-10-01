from pydantic import BaseModel

from src.llm.schemas.query import QueryOperation


class QueryUnderstanding(BaseModel):
    metric_phrase: str | None = None
    dimension_phrases: list[str] = []
    time_phrase: str | None = None
    operation: QueryOperation