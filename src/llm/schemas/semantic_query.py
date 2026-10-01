from pydantic import BaseModel
from src.llm.schemas.query import QueryOperation


class SemanticQuery(BaseModel):
    metric: str | None = None
    dimensions: list[str] = []
    time_phrase: str | None = None
    operation: QueryOperation