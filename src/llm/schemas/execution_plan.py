from pydantic import BaseModel

from src.llm.schemas.query_plan import QueryPlan
from src.llm.schemas.join_plan import JoinPlan


class ExecutionPlan(BaseModel):
    query_plan: QueryPlan
    join_plan: JoinPlan