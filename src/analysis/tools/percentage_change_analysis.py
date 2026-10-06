from typing import Any

from src.analysis.schemas.evidence import AnalysisEvidence
from src.analysis.tools.time_utils import (
    sort_rows_chronologically,
)


def percentage_change_analysis(
    rows: list[dict[str, Any]],
    metric: str,
    dimension: str,
) -> AnalysisEvidence:
    """
    Calculate percentage changes between consecutive
    chronological periods.

    The function operates only on rows returned by the
    Query Pipeline. It does not access the database,
    execute SQL, or call an LLM.
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if len(rows) < 2:
        raise ValueError(
            "At least two rows are required for "
            "percentage change analysis."
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

    ordered_rows = sort_rows_chronologically(
        rows=rows,
        dimension=dimension,
    )

    values = []

    for index, row in enumerate(ordered_rows):
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

        values.append(
            {
                "period": row[dimension],
                "value": value,
            }
        )

    changes = []

    for index in range(1, len(values)):
        previous = values[index - 1]
        current = values[index]

        previous_value = previous["value"]
        current_value = current["value"]

        absolute_change = (
            current_value - previous_value
        )

        percentage_change = None

        if previous_value != 0:
            percentage_change = (
                absolute_change
                / abs(previous_value)
            ) * 100

        if absolute_change > 0:
            direction = "increasing"
        elif absolute_change < 0:
            direction = "decreasing"
        else:
            direction = "stable"

        changes.append(
            {
                "from": previous["period"],
                "to": current["period"],
                "from_value": previous_value,
                "to_value": current_value,
                "absolute_change": absolute_change,
                "percentage_change": percentage_change,
                "direction": direction,
            }
        )

    valid_changes = [
        change
        for change in changes
        if change["percentage_change"] is not None
    ]

    largest_increase = None
    largest_decrease = None

    if valid_changes:
        largest_increase = max(
            valid_changes,
            key=lambda change: change["percentage_change"],
        )

        largest_decrease = min(
            valid_changes,
            key=lambda change: change["percentage_change"],
        )

    summary = (
        f"Calculated percentage changes across "
        f"{len(changes)} consecutive periods for {metric}."
    )

    return AnalysisEvidence(
        tool_name="percentage_change_analysis",
        summary=summary,
        data={
            "metric": metric,
            "dimension": dimension,
            "ordered_periods": [
                value["period"]
                for value in values
            ],
            "changes": changes,
            "largest_increase": largest_increase,
            "largest_decrease": largest_decrease,
        },
        source_columns=[
            dimension,
            metric,
        ],
        row_count=len(rows),
    )