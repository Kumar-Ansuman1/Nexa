from typing import Any

from src.analysis.schemas.evidence import AnalysisEvidence


def _percentile(
    values: list[int | float],
    percentile: float,
) -> float:
    """Calculate a percentile using linear interpolation."""

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
        + (upper_value - lower_value)
        * fraction
    )


def detect_outliers(
    rows: list[dict[str, Any]],
    metric: str,
    dimension: str | None = None,
    multiplier: float = 1.5,
) -> AnalysisEvidence:
    """
    Detect statistical outliers using the IQR method.

    An observation is considered an outlier when it falls
    outside:

        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR

    The function operates only on rows returned by the
    Query Pipeline. It does not access the database,
    execute SQL, or call an LLM.
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot detect outliers in empty result rows."
        )

    if not isinstance(metric, str) or not metric.strip():
        raise ValueError(
            "metric must be a non-empty string."
        )

    if dimension is not None:
        if not isinstance(dimension, str):
            raise TypeError(
                "dimension must be a string or None."
            )

        if not dimension.strip():
            raise ValueError(
                "dimension must be a non-empty string "
                "when provided."
            )

        dimension = dimension.strip()

    if not isinstance(multiplier, (int, float)):
        raise TypeError(
            "multiplier must be numeric."
        )

    if multiplier <= 0:
        raise ValueError(
            "multiplier must be greater than zero."
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

        if dimension is not None and dimension not in row:
            raise ValueError(
                f"Dimension column '{dimension}' "
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

    q1 = _percentile(values, 25)
    q3 = _percentile(values, 75)

    iqr = q3 - q1

    lower_bound = q1 - (
        multiplier * iqr
    )

    upper_bound = q3 + (
        multiplier * iqr
    )

    outliers = []

    for index, row in enumerate(rows):
        value = row[metric]

        if value < lower_bound or value > upper_bound:
            outlier = {
                "row_index": index,
                "value": value,
            }

            if dimension is not None:
                outlier["category"] = row[dimension]

            outliers.append(outlier)

    if outliers:
        summary = (
            f"Found {len(outliers)} outlier(s) in "
            f"{metric} using the IQR method."
        )
    else:
        summary = (
            f"No outliers were detected in {metric} "
            f"using the IQR method."
        )

    source_columns = [metric]

    if dimension is not None:
        source_columns.insert(0, dimension)

    return AnalysisEvidence(
        tool_name="detect_outliers",
        summary=summary,
        data={
            "metric": metric,
            "method": "IQR",
            "multiplier": multiplier,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "outlier_count": len(outliers),
            "outliers": outliers,
        },
        source_columns=source_columns,
        row_count=len(rows),
    )