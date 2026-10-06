from typing import Any

from src.analysis.schemas.evidence import AnalysisEvidence


def rank_categories(
    rows: list[dict[str, Any]],
    metric: str,
    dimension: str,
    order: str = "descending",
    limit: int | None = None,
) -> AnalysisEvidence:
    """
    Rank categories using a metric from query result rows.

    The function operates only on the rows returned by the
    Query Pipeline. It does not access the database or execute SQL.

    Example input:

        rows = [
            {"country": "India", "total_revenue": 50019.0},
            {"country": "United States", "total_revenue": 32355.0},
            {"country": "Canada", "total_revenue": 8157.0},
        ]

    Example:

        rank_categories(
            rows=rows,
            metric="total_revenue",
            dimension="country",
            order="descending",
            limit=3,
        )
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot rank categories from empty result rows."
        )

    if not isinstance(metric, str) or not metric.strip():
        raise ValueError(
            "metric must be a non-empty string."
        )

    if not isinstance(dimension, str) or not dimension.strip():
        raise ValueError(
            "dimension must be a non-empty string."
        )

    if order not in {"ascending", "descending"}:
        raise ValueError(
            "order must be either 'ascending' or 'descending'."
        )

    if limit is not None and limit <= 0:
        raise ValueError(
            "limit must be greater than zero."
        )

    metric = metric.strip()
    dimension = dimension.strip()

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

        if row[metric] is None:
            raise ValueError(
                f"Metric column '{metric}' "
                f"contains NULL at row {index}."
            )

        if not isinstance(row[metric], (int, float)):
            raise TypeError(
                f"Metric column '{metric}' must contain "
                f"numeric values."
            )

    ranked_rows = sorted(
        rows,
        key=lambda row: row[metric],
        reverse=order == "descending",
    )

    if limit is not None:
        ranked_rows = ranked_rows[:limit]

    ranking = []

    for position, row in enumerate(ranked_rows, start=1):
        ranking.append(
            {
                "rank": position,
                "category": row[dimension],
                "value": row[metric],
            }
        )

    top_result = ranking[0]

    summary = (
        f"Top category by {metric} is "
        f"{top_result['category']} with "
        f"{top_result['value']}."
    )

    return AnalysisEvidence(
        tool_name="rank_categories",
        summary=summary,
        data={
            "metric": metric,
            "dimension": dimension,
            "order": order,
            "ranking": ranking,
        },
        source_columns=[
            dimension,
            metric,
        ],
        row_count=len(rows),
    )