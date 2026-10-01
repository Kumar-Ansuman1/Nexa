from src.llm.schemas.query import (
    QueryFilter,
    QueryIntent,
    QueryOperation,
    TimeRange,
)


query = QueryIntent(
    metric="sem_transaction_amount",
    dimensions=["sem_subscription_plan"],
    operation=QueryOperation.SUM,
    filters=[
        QueryFilter(
            semantic_id="sem_subscription_plan",
            operator="equals",
            value="Business",
        )
    ],
    time_range=TimeRange(
        semantic_id="sem_transaction_date",
        start="2026-03-01",
        end="2026-03-31",
    ),
)


print(query.model_dump())