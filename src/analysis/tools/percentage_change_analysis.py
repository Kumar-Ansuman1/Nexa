from typing import Annotated, Any

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.analysis.schemas.evidence import AnalysisEvidence
from src.analysis.tools.time_utils import sort_rows_chronologically


@tool
def percentage_change_analysis(
    rows: Annotated[list[dict[str, Any]], InjectedState("rows")],
    metric: str,
    dimension: str,
) -> AnalysisEvidence:
    """
    Calculate percentage changes between consecutive chronological periods.

    Operates only on rows returned by the Query Pipeline.
    """
    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if len(rows) < 2:
        raise ValueError(
            "At least two rows are required for percentage change analysis."
        )

    if not isinstance(metric, str) or not metric.strip():
        raise ValueError("metric must be a non-empty string.")

    if not isinstance(dimension, str) or not dimension.strip():
        raise ValueError("dimension must be a non-empty string.")

    metric = metric.strip()
    dimension = dimension.strip()

    ordered_rows = sort_rows_chronologically(
        rows=rows,
        dimension=dimension,
    )

    values: list[dict[str, Any]] = []

    for index, row in enumerate(ordered_rows):
        if not isinstance(row, dict):
            raise TypeError(
                f"Row at index {index} must be a dictionary."
            )

        if metric not in row:
            raise ValueError(
                f"Metric column '{metric}' is missing from row {index}."
            )

        value = row[metric]

        if value is None:
            raise ValueError(
                f"Metric column '{metric}' contains NULL at row {index}."
            )

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                f"Metric column '{metric}' must contain numeric values."
            )

        values.append(
            {
                "period": row[dimension],
                "value": value,
            }
        )

    changes: list[dict[str, Any]] = []

    for index in range(1, len(values)):
        previous = values[index - 1]
        current = values[index]

        previous_value = previous["value"]
        current_value = current["value"]

        absolute_change = current_value - previous_value

        percentage_change = None
        if previous_value != 0:
            percentage_change = (
                absolute_change / abs(previous_value)
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
                value["period"] for value in values
            ],
            "changes": changes,
            "largest_increase": largest_increase,
            "largest_decrease": largest_decrease,
        },
        source_columns=[dimension, metric],
        row_count=len(rows),
    )
