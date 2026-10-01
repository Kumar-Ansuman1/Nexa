from src.llm.schemas.execution_plan import ExecutionPlan
from src.llm.schemas.query_plan import QueryPlan
from src.llm.schemas.join_plan import JoinPlan


def build_execution_plan(
    query_plan: QueryPlan,
    join_plan: JoinPlan,
) -> ExecutionPlan:

    return ExecutionPlan(
        query_plan=query_plan,
        join_plan=join_plan,
    )