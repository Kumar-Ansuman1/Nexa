from datetime import datetime
from typing import Any

from src.analysis.schemas.evidence import AnalysisEvidence


MONTH_NAMES = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}

QUARTER_MONTHS = {
    "q1": 1,
    "q2": 4,
    "q3": 7,
    "q4": 10,
}


def _parse_time_value(value: Any) -> tuple[int, int, int, str]:
    """
    Convert common temporal values into a sortable representation.

    Supported examples:

        2024
        "2024"
        "2024-01"
        "2024-01-15"
        "January 2024"
        "Jan 2024"
        "Q1 2024"

    Returns:

        (year, month, day, original_value)
    """

    original = str(value).strip()

    if isinstance(value, int) and 1900 <= value <= 2100:
        return value, 1, 1, original

    if isinstance(value, float) and value.is_integer():
        year = int(value)

        if 1900 <= year <= 2100:
            return year, 1, 1, original

    # YYYY-MM-DD
    try:
        parsed = datetime.strptime(original, "%Y-%m-%d")
        return (
            parsed.year,
            parsed.month,
            parsed.day,
            original,
        )
    except ValueError:
        pass

    # YYYY-MM
    try:
        parsed = datetime.strptime(original, "%Y-%m")
        return (
            parsed.year,
            parsed.month,
            1,
            original,
        )
    except ValueError:
        pass

    # YYYY
    try:
        parsed = datetime.strptime(original, "%Y")
        return (
            parsed.year,
            1,
            1,
            original,
        )
    except ValueError:
        pass

    # Month Year
    parts = original.lower().replace(",", "").split()

    if len(parts) == 2:
        first, second = parts

        if second.isdigit():
            year = int(second)

            if first in MONTH_NAMES:
                return (
                    year,
                    MONTH_NAMES[first],
                    1,
                    original,
                )

            abbreviated_months = {
                name[:3]: month
                for name, month in MONTH_NAMES.items()
            }

            if first in abbreviated_months:
                return (
                    year,
                    abbreviated_months[first],
                    1,
                    original,
                )

            if first in QUARTER_MONTHS:
                return (
                    year,
                    QUARTER_MONTHS[first],
                    1,
                    original,
                )

    raise ValueError(
        f"Unable to interpret '{value}' as a chronological "
        "value. Supported formats include YYYY, YYYY-MM, "
        "YYYY-MM-DD, Month YYYY, and Q1/Q2/Q3/Q4 YYYY."
    )


def analyze_trend(
    rows: list[dict[str, Any]],
    metric: str,
    dimension: str,
) -> AnalysisEvidence:
    """
    Analyze the trend of a numeric metric across a chronological
    dimension.

    Rows are explicitly ordered by this tool. The function does
    not rely on the order returned by SQL.
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if len(rows) < 2:
        raise ValueError(
            "At least two rows are required to analyze a trend."
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

    normalized_rows = []

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

        sort_key = _parse_time_value(row[dimension])

        normalized_rows.append(
            {
                "period": row[dimension],
                "value": value,
                "_sort_key": sort_key[:3],
            }
        )

    normalized_rows.sort(
        key=lambda row: row["_sort_key"]
    )

    # Remove internal sorting metadata from the evidence.
    ordered_rows = [
        {
            "period": row["period"],
            "value": row["value"],
        }
        for row in normalized_rows
    ]

    starting = ordered_rows[0]
    ending = ordered_rows[-1]

    starting_value = starting["value"]
    ending_value = ending["value"]

    change = ending_value - starting_value

    percentage_change = None

    if starting_value != 0:
        percentage_change = (
            change / abs(starting_value)
        ) * 100

    if change > 0:
        direction = "increasing"
    elif change < 0:
        direction = "decreasing"
    else:
        direction = "stable"

    summary = (
        f"{metric} is {direction}, changing from "
        f"{starting_value} at {starting['period']} to "
        f"{ending_value} at {ending['period']}."
    )

    return AnalysisEvidence(
        tool_name="analyze_trend",
        summary=summary,
        data={
            "metric": metric,
            "dimension": dimension,
            "start": starting,
            "end": ending,
            "change": change,
            "percentage_change": percentage_change,
            "direction": direction,
            "ordered_rows": ordered_rows,
        },
        source_columns=[
            dimension,
            metric,
        ],
        row_count=len(rows),
    )