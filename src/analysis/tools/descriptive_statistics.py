from typing import Any
from statistics import median

from src.analysis.schemas.evidence import AnalysisEvidence


def descriptive_statistics(
    rows: list[dict[str, Any]],
    metric: str,
) -> AnalysisEvidence:
    """
    Calculate descriptive statistics for a numeric metric.

    The function operates only on rows returned by the
    Query Pipeline. It does not access the database,
    execute SQL, or call an LLM.

    Calculated statistics:

    - count
    - sum
    - mean
    - median
    - minimum
    - maximum
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot calculate statistics from empty result rows."
        )

    if not isinstance(metric, str) or not metric.strip():
        raise ValueError(
            "metric must be a non-empty string."
        )

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

        if not isinstance(value, (int, float)):
            raise TypeError(
                f"Metric column '{metric}' must contain "
                f"numeric values."
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