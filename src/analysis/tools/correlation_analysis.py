from math import sqrt
from typing import Any

from src.analysis.schemas.evidence import AnalysisEvidence


def correlation_analysis(
    rows: list[dict[str, Any]],
    metric_x: str,
    metric_y: str,
) -> AnalysisEvidence:
    """
    Calculate Pearson correlation between two numeric metrics.

    The function operates only on rows returned by the
    Query Pipeline. It does not access the database,
    execute SQL, or call an LLM.

    Pearson correlation ranges from -1 to +1:

        +1 -> perfect positive linear relationship
         0 -> no linear relationship
        -1 -> perfect negative linear relationship
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if len(rows) < 2:
        raise ValueError(
            "At least two rows are required for correlation analysis."
        )

    if not isinstance(metric_x, str) or not metric_x.strip():
        raise ValueError(
            "metric_x must be a non-empty string."
        )

    if not isinstance(metric_y, str) or not metric_y.strip():
        raise ValueError(
            "metric_y must be a non-empty string."
        )

    metric_x = metric_x.strip()
    metric_y = metric_y.strip()

    if metric_x == metric_y:
        raise ValueError(
            "metric_x and metric_y must be different columns."
        )

    x_values: list[int | float] = []
    y_values: list[int | float] = []

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise TypeError(
                f"Row at index {index} must be a dictionary."
            )

        if metric_x not in row:
            raise ValueError(
                f"Metric column '{metric_x}' "
                f"is missing from row {index}."
            )

        if metric_y not in row:
            raise ValueError(
                f"Metric column '{metric_y}' "
                f"is missing from row {index}."
            )

        x = row[metric_x]
        y = row[metric_y]

        if x is None:
            raise ValueError(
                f"Metric column '{metric_x}' "
                f"contains NULL at row {index}."
            )

        if y is None:
            raise ValueError(
                f"Metric column '{metric_y}' "
                f"contains NULL at row {index}."
            )

        if not isinstance(x, (int, float)):
            raise TypeError(
                f"Metric column '{metric_x}' must contain "
                f"numeric values."
            )

        if not isinstance(y, (int, float)):
            raise TypeError(
                f"Metric column '{metric_y}' must contain "
                f"numeric values."
            )

        x_values.append(x)
        y_values.append(y)

    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)

    numerator = sum(
        (x - x_mean) * (y - y_mean)
        for x, y in zip(x_values, y_values)
    )

    x_squared_difference = sum(
        (x - x_mean) ** 2
        for x in x_values
    )

    y_squared_difference = sum(
        (y - y_mean) ** 2
        for y in y_values
    )

    denominator = sqrt(
        x_squared_difference
        * y_squared_difference
    )

    if denominator == 0:
        raise ValueError(
            "Correlation cannot be calculated because "
            "one or both metrics have zero variance."
        )

    correlation = numerator / denominator

    if correlation > 0:
        direction = "positive"
    elif correlation < 0:
        direction = "negative"
    else:
        direction = "none"

    absolute_correlation = abs(correlation)

    if absolute_correlation >= 0.8:
        strength = "strong"
    elif absolute_correlation >= 0.5:
        strength = "moderate"
    elif absolute_correlation >= 0.3:
        strength = "weak"
    else:
        strength = "very weak"

    summary = (
        f"{metric_x} and {metric_y} have a "
        f"{strength} {direction} linear relationship "
        f"(correlation={correlation:.4f})."
    )

    return AnalysisEvidence(
        tool_name="correlation_analysis",
        summary=summary,
        data={
            "metric_x": metric_x,
            "metric_y": metric_y,
            "correlation": correlation,
            "direction": direction,
            "strength": strength,
        },
        source_columns=[
            metric_x,
            metric_y,
        ],
        row_count=len(rows),
    )