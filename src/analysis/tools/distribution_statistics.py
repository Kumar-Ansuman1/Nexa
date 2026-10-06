from statistics import pvariance, pstdev
from typing import Any

from src.analysis.schemas.evidence import AnalysisEvidence


def _percentile(
    values: list[int | float],
    percentile: float,
) -> float:
    """
    Calculate a percentile using linear interpolation.
    """

    if not 0 <= percentile <= 100:
        raise ValueError(
            "percentile must be between 0 and 100."
        )

    sorted_values = sorted(values)

    position = (
        (len(sorted_values) - 1)
        * percentile
        / 100
    )

    lower_index = int(position)
    upper_index = min(
        lower_index + 1,
        len(sorted_values) - 1,
    )

    fraction = position - lower_index

    lower_value = sorted_values[lower_index]
    upper_value = sorted_values[upper_index]

    return (
        lower_value
        + (upper_value - lower_value) * fraction
    )


def distribution_statistics(
    rows: list[dict[str, Any]],
    metric: str,
) -> AnalysisEvidence:
    """
    Calculate statistics describing the spread and distribution
    of a numeric metric.

    The function operates only on rows returned by the
    Query Pipeline. It does not access the database,
    execute SQL, or call an LLM.

    Calculated statistics:

    - variance
    - standard deviation
    - minimum
    - maximum
    - range
    - first quartile (Q1)
    - third quartile (Q3)
    - interquartile range (IQR)
    - 10th percentile
    - 90th percentile
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot calculate distribution statistics "
            "from empty result rows."
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

    minimum = min(values)
    maximum = max(values)

    q1 = _percentile(values, 25)
    q3 = _percentile(values, 75)

    interquartile_range = q3 - q1

    value_range = maximum - minimum

    variance = pvariance(values)
    standard_deviation = pstdev(values)

    percentile_10 = _percentile(values, 10)
    percentile_90 = _percentile(values, 90)

    summary = (
        f"{metric} has a standard deviation of "
        f"{standard_deviation}, a range of "
        f"{value_range}, and an interquartile range "
        f"of {interquartile_range}."
    )

    return AnalysisEvidence(
        tool_name="distribution_statistics",
        summary=summary,
        data={
            "metric": metric,
            "variance": variance,
            "standard_deviation": standard_deviation,
            "minimum": minimum,
            "maximum": maximum,
            "range": value_range,
            "q1": q1,
            "q3": q3,
            "iqr": interquartile_range,
            "percentile_10": percentile_10,
            "percentile_90": percentile_90,
        },
        source_columns=[metric],
        row_count=len(rows),
    )