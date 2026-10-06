from statistics import median
from typing import Any

from src.analysis.schemas.evidence import AnalysisEvidence


def group_statistics(
    rows: list[dict[str, Any]],
    metric: str,
    dimension: str,
) -> AnalysisEvidence:
    """
    Calculate descriptive statistics for each group.

    The function operates only on rows returned by the
    Query Pipeline. It does not access the database,
    execute SQL, or call an LLM.

    Statistics calculated for every group:

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
            "Cannot calculate group statistics "
            "from empty result rows."
        )

    if not isinstance(metric, str) or not metric.strip():
        raise ValueError(
            "metric must be a non-empty string."
        )

    if not isinstance(dimension, str) or not dimension.strip():
        raise ValueError(
            "dimension must be a non-empty string."
        )

    metric = metric.strip()
    dimension = dimension.strip()

    grouped_values: dict[Any, list[int | float]] = {}

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

        group = row[dimension]
        value = row[metric]

        if group is None:
            raise ValueError(
                f"Dimension column '{dimension}' "
                f"contains NULL at row {index}."
            )

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

        grouped_values.setdefault(group, []).append(value)

    groups = {}

    for group, values in grouped_values.items():
        total = sum(values)
        count = len(values)

        groups[str(group)] = {
            "group": group,
            "count": count,
            "sum": total,
            "mean": total / count,
            "median": median(values),
            "minimum": min(values),
            "maximum": max(values),
        }

    summary = (
        f"Calculated statistics for {len(groups)} "
        f"groups using {metric}."
    )

    return AnalysisEvidence(
        tool_name="group_statistics",
        summary=summary,
        data={
            "metric": metric,
            "dimension": dimension,
            "groups": groups,
        },
        source_columns=[
            dimension,
            metric,
        ],
        row_count=len(rows),
    )