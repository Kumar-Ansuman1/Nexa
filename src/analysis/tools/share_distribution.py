from typing import Annotated, Any

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.analysis.schemas.evidence import AnalysisEvidence


@tool
def share_distribution(
    rows: Annotated[list[dict[str, Any]], InjectedState("rows")],
    metric: str,
    dimension: str,
) -> AnalysisEvidence:
    """
    Calculate each category's share of the total metric.

    Categories are sorted from highest share to lowest share.
    Operates only on rows returned by the Query Pipeline.
    """
    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot calculate share distribution from empty result rows."
        )

    if not isinstance(metric, str) or not metric.strip():
        raise ValueError("metric must be a non-empty string.")

    if not isinstance(dimension, str) or not dimension.strip():
        raise ValueError("dimension must be a non-empty string.")

    metric = metric.strip()
    dimension = dimension.strip()

    category_values: dict[Any, int | float] = {}

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise TypeError(
                f"Row at index {index} must be a dictionary."
            )

        if dimension not in row:
            raise ValueError(
                f"Dimension column '{dimension}' is missing from row {index}."
            )

        if metric not in row:
            raise ValueError(
                f"Metric column '{metric}' is missing from row {index}."
            )

        category = row[dimension]
        value = row[metric]

        if category is None:
            raise ValueError(
                f"Dimension column '{dimension}' contains NULL at row {index}."
            )

        if value is None:
            raise ValueError(
                f"Metric column '{metric}' contains NULL at row {index}."
            )

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                f"Metric column '{metric}' must contain numeric values."
            )

        try:
            category_values[category] = (
                category_values.get(category, 0) + value
            )
        except TypeError as exc:
            raise TypeError(
                f"Dimension value at row {index} must be hashable."
            ) from exc

    total_value = sum(category_values.values())

    if total_value == 0:
        raise ValueError(
            "Cannot calculate share distribution because "
            "the total metric value is zero."
        )

    ranked_categories = sorted(
        category_values.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    distribution: list[dict[str, Any]] = []
    cumulative_percentage = 0.0

    for rank, (category, value) in enumerate(
        ranked_categories,
        start=1,
    ):
        percentage = (value / total_value) * 100
        cumulative_percentage += percentage

        distribution.append(
            {
                "rank": rank,
                "category": category,
                "value": value,
                "percentage": percentage,
                "cumulative_percentage": cumulative_percentage,
            }
        )

    summary = (
        f"Calculated the share distribution of {metric} "
        f"across {len(distribution)} {dimension} categories."
    )

    return AnalysisEvidence(
        tool_name="share_distribution",
        summary=summary,
        data={
            "metric": metric,
            "dimension": dimension,
            "total_value": total_value,
            "distribution": distribution,
        },
        source_columns=[dimension, metric],
        row_count=len(rows),
    )
