from pydantic import BaseModel

from src.llm.schemas.query import QueryOperation


class ResolvedColumn(BaseModel):
    dataset: str
    column: str


class QueryPlan(BaseModel):
    metric: ResolvedColumn | None = None
    dimensions: list[ResolvedColumn] = []
    operation: QueryOperation
    time_phrase: str | None = None
    required_datasets: list[str] = []