from src.data.semantic.execution_planner import build_execution_plan
from src.llm.schemas.query_plan import QueryPlan, ResolvedColumn
from src.llm.schemas.join_plan import JoinPlan, JoinStep
from src.llm.schemas.query import QueryOperation


query_plan = QueryPlan(
    metric=ResolvedColumn(
        dataset="transactions",
        column="amount",
    ),
    dimensions=[
        ResolvedColumn(
            dataset="customers",
            column="plan",
        )
    ],
    operation=QueryOperation.SUM,
    time_phrase="March 2026",
    required_datasets=[
        "transactions",
        "customers",
    ],
)


join_plan = JoinPlan(
    joins=[
        JoinStep(
            left_dataset="customers",
            left_column="customer_id",
            right_dataset="transactions",
            right_column="customer_id",
        )
    ]
)


result = build_execution_plan(
    query_plan=query_plan,
    join_plan=join_plan,
)

print("\nExecution Plan:")
print(result.model_dump())