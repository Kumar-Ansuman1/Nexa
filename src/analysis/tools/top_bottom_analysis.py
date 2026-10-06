from typing import Any

from src.analysis.schemas.evidence import AnalysisEvidence


def top_bottom_analysis(
    rows: list[dict[str, Any]],
    metric: str,
    dimension: str,
    limit: int = 3,
) -> AnalysisEvidence:
    """
    Return the top and bottom categories according to a numeric metric.

    The function operates only on rows returned by the
    Query Pipeline. It does not access the database,
    execute SQL, or call an LLM.
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot perform top/bottom analysis "
            "on empty result rows."
        )

    if not isinstance(metric, str) or not metric.strip():
        raise ValueError(
            "metric must be a non-empty string."
        )

    if not isinstance(dimension, str) or not dimension.strip():
        raise ValueError(
            "dimension must be a non-empty string."
        )

    if not isinstance(limit, int):
        raise TypeError(
            "limit must be an integer."
        )

    if limit <= 0:
        raise ValueError(
            "limit must be greater than zero."
        )

    metric = metric.strip()
    dimension = dimension.strip()

    validated_rows = []

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

        validated_rows.append(
            {
                "category": row[dimension],
                "value": value,
            }
        )

    ranked_rows = sorted(
        validated_rows,
        key=lambda row: row["value"],
        reverse=True,
    )

    top = ranked_rows[:limit]

    bottom = list(
        reversed(ranked_rows[-limit:])
    )

    return_top = [
        {
            "rank": index + 1,
            "category": row["category"],
            "value": row["value"],
        }
        for index, row in enumerate(top)
    ]

    return_bottom = [
        {
            "rank": index + 1,
            "category": row["category"],
            "value": row["value"],
        }
        for index, row in enumerate(bottom)
    ]

    summary = (
        f"Top {len(return_top)} and bottom "
        f"{len(return_bottom)} categories identified "
        f"using {metric}."
    )

    return AnalysisEvidence(
        tool_name="top_bottom_analysis",
        summary=summary,
        data={
            "metric": metric,
            "dimension": dimension,
            "limit": limit,
            "top": return_top,
            "bottom": return_bottom,
        },
        source_columns=[
            dimension,
            metric,
        ],
        row_count=len(rows),
    )