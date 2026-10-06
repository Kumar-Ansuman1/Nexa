from typing import Any

from src.analysis.schemas.evidence import AnalysisEvidence


def calculate_change(
    rows: list[dict[str, Any]],
    metric: str,
    dimension: str,
    start: Any,
    end: Any,
) -> AnalysisEvidence:
    """
    Calculate the absolute and percentage change in a metric
    between two specific dimension values.

    The function operates only on rows returned by the
    Query Pipeline. It does not access the database,
    execute SQL, or call an LLM.
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot calculate change from empty result rows."
        )

    if not isinstance(metric, str) or not metric.strip():
        raise ValueError(
            "metric must be a non-empty string."
        )

    if not isinstance(dimension, str) or not dimension.strip():
        raise ValueError(
            "dimension must be a non-empty string."
        )

    if start == end:
        raise ValueError(
            "start and end must be different."
        )

    metric = metric.strip()
    dimension = dimension.strip()

    start_value = None
    end_value = None

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

        if not isinstance(value, (int, float)):
            raise TypeError(
                f"Metric column '{metric}' must contain "
                f"numeric values."
            )

        if row[dimension] == start:
            if start_value is not None:
                raise ValueError(
                    f"Multiple rows found for start value "
                    f"'{start}'."
                )

            start_value = value

        if row[dimension] == end:
            if end_value is not None:
                raise ValueError(
                    f"Multiple rows found for end value "
                    f"'{end}'."
                )

            end_value = value

    if start_value is None:
        raise ValueError(
            f"Start value '{start}' was not found "
            "in the query result."
        )

    if end_value is None:
        raise ValueError(
            f"End value '{end}' was not found "
            "in the query result."
        )

    change = end_value - start_value

    percentage_change = None

    if start_value != 0:
        percentage_change = (
            change / abs(start_value)
        ) * 100

    if change > 0:
        direction = "increasing"
    elif change < 0:
        direction = "decreasing"
    else:
        direction = "stable"

    summary = (
        f"{metric} changed from {start_value} at "
        f"{start} to {end_value} at {end}, "
        f"a {direction} change of {change}."
    )

    return AnalysisEvidence(
        tool_name="calculate_change",
        summary=summary,
        data={
            "metric": metric,
            "dimension": dimension,
            "start": {
                "period": start,
                "value": start_value,
            },
            "end": {
                "period": end,
                "value": end_value,
            },
            "change": change,
            "percentage_change": percentage_change,
            "direction": direction,
        },
        source_columns=[
            dimension,
            metric,
        ],
        row_count=len(rows),
    )