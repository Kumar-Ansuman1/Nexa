from datetime import datetime
from typing import Any


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


def parse_time_value(
    value: Any,
) -> tuple[int, int, int]:
    """
    Convert common temporal values into a sortable
    (year, month, day) tuple.
    """

    original = str(value).strip()

    if isinstance(value, int) and 1900 <= value <= 2100:
        return value, 1, 1

    if isinstance(value, float) and value.is_integer():
        year = int(value)

        if 1900 <= year <= 2100:
            return year, 1, 1

    try:
        parsed = datetime.strptime(
            original,
            "%Y-%m-%d",
        )

        return (
            parsed.year,
            parsed.month,
            parsed.day,
        )

    except ValueError:
        pass

    try:
        parsed = datetime.strptime(
            original,
            "%Y-%m",
        )

        return (
            parsed.year,
            parsed.month,
            1,
        )

    except ValueError:
        pass

    try:
        parsed = datetime.strptime(
            original,
            "%Y",
        )

        return (
            parsed.year,
            1,
            1,
        )

    except ValueError:
        pass

    parts = (
        original
        .lower()
        .replace(",", "")
        .split()
    )

    if len(parts) == 2:
        first, second = parts

        if second.isdigit():
            year = int(second)

            if first in MONTH_NAMES:
                return (
                    year,
                    MONTH_NAMES[first],
                    1,
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
                )

            if first in QUARTER_MONTHS:
                return (
                    year,
                    QUARTER_MONTHS[first],
                    1,
                )

    raise ValueError(
        f"Unable to interpret '{value}' as a chronological "
        "value."
    )


def sort_rows_chronologically(
    rows: list[dict[str, Any]],
    dimension: str,
) -> list[dict[str, Any]]:
    """
    Return rows sorted chronologically by the given dimension.
    """

    sortable_rows = []

    for index, row in enumerate(rows):
        if dimension not in row:
            raise ValueError(
                f"Dimension column '{dimension}' "
                f"is missing from row {index}."
            )

        sort_key = parse_time_value(
            row[dimension]
        )

        sortable_rows.append(
            (
                sort_key,
                row,
            )
        )

    sortable_rows.sort(
        key=lambda item: item[0]
    )

    return [
        row
        for _, row in sortable_rows
    ]