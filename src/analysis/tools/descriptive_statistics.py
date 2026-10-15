from typing import Annotated, Any
from statistics import median

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.analysis.schemas.evidence import AnalysisEvidence


@tool
def descriptive_statistics(
    rows: Annotated[list[dict[str, Any]], InjectedState("rows")],
    metric: str,
) -> AnalysisEvidence:
    """
    Calculate descriptive statistics for a numeric metric.

    Use this tool to find the count, sum, mean, median,
    minimum, and maximum of a numeric column.

    Args:
        metric: Numeric column to analyze.
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot calculate statistics from empty result rows."
        )

    if not isinstance(metric, str) or not metric.strip():
        raise ValueError("metric must be a non-empty string.")

    metric = metric.strip()

    values: list[int | float] = []

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise TypeError(
                f"Row at index {index} must be a dictionary."
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

        values.append(value)

    count = len(values)
    total = sum(values)
    mean = total / count
    median_value = median(values)
    minimum = min(values)
    maximum = max(values)

    summary = (
        f"The {metric} has a mean of {mean}, "
        f"a median of {median_value}, "
        f"a minimum of {minimum}, "
        f"and a maximum of {maximum}."
    )

    return AnalysisEvidence(
        tool_name="descriptive_statistics",
        summary=summary,
        data={
            "metric": metric,
            "count": count,
            "sum": total,
            "mean": mean,
            "median": median_value,
            "minimum": minimum,
            "maximum": maximum,
        },
        source_columns=[metric],
        row_count=len(rows),
    )