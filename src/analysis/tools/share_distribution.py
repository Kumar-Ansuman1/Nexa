from typing import Any

from src.analysis.schemas.evidence import AnalysisEvidence


def share_distribution(
    rows: list[dict[str, Any]],
    metric: str,
    dimension: str,
) -> AnalysisEvidence:
    """
    Calculate each category's share of the total metric.

    Categories are sorted from highest share to lowest share.

    The function operates only on rows returned by the
    Query Pipeline. It does not access the database,
    execute SQL, or call an LLM.
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot calculate share distribution "
            "from empty result rows."
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

    category_values: dict[Any, float] = {}

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

        category = row[dimension]
        value = row[metric]

        if category is None:
            raise ValueError(
                f"Dimension column '{dimension}' "
                f"contains NULL at row {index}."
            )

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

        category_values[category] = (
            category_values.get(category, 0)
            + value
        )

    total_value = sum(category_values.values())

    if total_value == 0:
        raise ValueError(
            "Cannot calculate share distribution because "
            "the total metric value is zero."
        )

    ranked_categories = sorted(
        category_values.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    distribution = []

    cumulative_percentage = 0.0

    for rank, (category, value) in enumerate(
        ranked_categories,
        start=1,
    ):
        percentage = (
            value / total_value
        ) * 100

        cumulative_percentage += percentage

        distribution.append(
            {
                "rank": rank,
                "category": category,
                "value": value,
                "percentage": percentage,
                "cumulative_percentage": (
                    cumulative_percentage
                ),
            }
        )

    summary = (
        f"Calculated the share distribution of "
        f"{metric} across {len(distribution)} "
        f"{dimension} categories."
    )

    return AnalysisEvidence(
        tool_name="share_distribution",
        summary=summary,
        data={
            "metric": metric,
            "dimension": dimension,
            "total_value": total_value,
            "distribution": distribution,
        },
        source_columns=[
            dimension,
            metric,
        ],
        row_count=len(rows),
    )