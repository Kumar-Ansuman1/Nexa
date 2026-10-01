from enum import Enum

from pydantic import BaseModel


class QueryOperation(str, Enum):
    SUM = "sum"
    AVG = "avg"
    COUNT = "count"
    MIN = "min"
    MAX = "max"


class QueryFilter(BaseModel):
    semantic_id: str
    operator: str
    value: str


class QueryIntent(BaseModel):
    metric: str | None = None
    dimensions: list[str] = []
    operation: QueryOperation
    time_semantic_id: str | None = None
    filters: list[QueryFilter] = []