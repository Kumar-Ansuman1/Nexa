from typing import Annotated, Any

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.analysis.schemas.evidence import AnalysisEvidence


@tool
def calculate_contribution(
    rows: Annotated[list[dict[str, Any]], InjectedState("rows")],
    metric: str,
    dimension: str,
    category: Any,
) -> AnalysisEvidence:
    """
    Calculate the percentage contribution of a category
    to the total metric.

    Use this tool to answer questions such as:
    'What percentage of total revenue comes from India?'

    Args:
        metric: Numeric column to analyze.
        dimension: Column containing the categories.
        category: Category whose contribution is calculated.
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot calculate contribution from empty result rows."
        )

    if not isinstance(metric, str) or not metric.strip():
        raise ValueError("metric must be a non-empty string.")

    if not isinstance(dimension, str) or not dimension.strip():
        raise ValueError("dimension must be a non-empty string.")

    metric = metric.strip()
    dimension = dimension.strip()

    category_row = None
    total_value = 0.0

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

        if isinstance(value, bool) or not isinstance(
            value, (int, float)
        ):
            raise TypeError(
                f"Metric column '{metric}' must contain "
                "numeric values."
            )

        total_value += value

        if row[dimension] == category:
            category_row = row

    if category_row is None:
        raise ValueError(
            f"Category '{category}' was not found in "
            "the query result."
        )

    category_value = category_row[metric]

    if total_value == 0:
        raise ValueError(
            "Cannot calculate contribution because "
            "the total metric value is zero."
        )

    contribution_percentage = (
        category_value / total_value
    ) * 100

    summary = (
        f"{category} contributes "
        f"{contribution_percentage:.2f}% of total "
        f"{metric}."
    )

    return AnalysisEvidence(
        tool_name="calculate_contribution",
        summary=summary,
        data={
            "metric": metric,
            "dimension": dimension,
            "category": category,
            "category_value": category_value,
            "total_value": total_value,
            "contribution_percentage": contribution_percentage,
        },
        source_columns=[
            dimension,
            metric,
        ],
        row_count=len(rows),
    )