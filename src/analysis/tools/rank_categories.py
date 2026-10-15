from typing import Annotated, Any

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.analysis.schemas.evidence import AnalysisEvidence


@tool
def rank_categories(
    rows: Annotated[list[dict[str, Any]], InjectedState("rows")],
    metric: str,
    dimension: str,
    order: str = "descending",
    limit: int | None = None,
) -> AnalysisEvidence:
    """Rank categories by a numeric metric from the query results.

    Choose the metric and dimension from the available result columns.
    Use descending order for highest-first rankings and ascending order
    for lowest-first rankings. Optionally limit the number of results.

    The query result rows are injected by LangGraph and are not supplied
    by the language model.
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot rank categories from empty result rows."
        )

    if not isinstance(metric, str) or not metric.strip():
        raise ValueError(
            "metric must be a non-empty string."
        )

    if not isinstance(dimension, str) or not dimension.strip():
        raise ValueError(
            "dimension must be a non-empty string."
        )

    if order not in {"ascending", "descending"}:
        raise ValueError(
            "order must be either 'ascending' or 'descending'."
        )

    if limit is not None:
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise TypeError("limit must be an integer or None.")

        if limit <= 0:
            raise ValueError(
                "limit must be greater than zero."
            )

    metric = metric.strip()
    dimension = dimension.strip()

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise TypeError(
                f"Row at index {index} must be a dictionary."
            )

        if dimension not in row:
            raise ValueError(
                f"Dimension column '{dimension}' "
                f"is missing from row {index}."
            )

        if metric not in row:
            raise ValueError(
                f"Metric column '{metric}' "
                f"is missing from row {index}."
            )

        value = row[metric]

        if value is None:
            raise ValueError(
                f"Metric column '{metric}' "
                f"contains NULL at row {index}."
            )

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                f"Metric column '{metric}' must contain "
                f"numeric values."
            )

    ranked_rows = sorted(
        rows,
        key=lambda row: row[metric],
        reverse=order == "descending",
    )

    if limit is not None:
        ranked_rows = ranked_rows[:limit]

    ranking = [
        {
            "rank": position,
            "category": row[dimension],
            "value": row[metric],
        }
        for position, row in enumerate(ranked_rows, start=1)
    ]

    top_result = ranking[0]

    summary = (
        f"Top category by {metric} is "
        f"{top_result['category']} with "
        f"{top_result['value']}."
    )

    return AnalysisEvidence(
        tool_name="rank_categories",
        summary=summary,
        data={
            "metric": metric,
            "dimension": dimension,
            "order": order,
            "ranking": ranking,
        },
        source_columns=[dimension, metric],
        row_count=len(rows),
    )
