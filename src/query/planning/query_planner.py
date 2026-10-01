from src.llm.schemas.query_plan import (
    QueryPlan,
    ResolvedColumn,
)
from src.llm.schemas.semantic_query import SemanticQuery


def build_query_plan(
    semantic_query: SemanticQuery,
    resolved_query: dict,
) -> QueryPlan:

    metric = None

    if resolved_query["metric"]:
        dataset, column = resolved_query["metric"]

        metric = ResolvedColumn(
            dataset=dataset,
            column=column,
        )

    dimensions = []

    for dataset, column in resolved_query["dimensions"]:
        dimensions.append(
            ResolvedColumn(
                dataset=dataset,
                column=column,
            )
        )

    required_datasets = []

    if metric:
        required_datasets.append(metric.dataset)

    for dimension in dimensions:
        if dimension.dataset not in required_datasets:
            required_datasets.append(dimension.dataset)

    return QueryPlan(
        metric=metric,
        dimensions=dimensions,
        operation=semantic_query.operation,
        time_phrase=semantic_query.time_phrase,
        required_datasets=required_datasets,
    )