from typing import Any

from src.analysis.schemas.evidence import AnalysisEvidence


def frequency_analysis(
    rows: list[dict[str, Any]],
    dimension: str,
) -> AnalysisEvidence:
    """
    Calculate the frequency of each category in a dimension.

    The function operates only on rows returned by the
    Query Pipeline. It does not access the database,
    execute SQL, or call an LLM.

    The result contains:

    - count for each category
    - percentage of total rows
    - cumulative percentage
    - ranking by frequency
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot calculate frequency analysis "
            "from empty result rows."
        )

    if not isinstance(dimension, str) or not dimension.strip():
        raise ValueError(
            "dimension must be a non-empty string."
        )

    dimension = dimension.strip()

    frequencies: dict[Any, int] = {}

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

        category = row[dimension]

        if category is None:
            raise ValueError(
                f"Dimension column '{dimension}' "
                f"contains NULL at row {index}."
            )

        frequencies[category] = (
            frequencies.get(category, 0) + 1
        )

    total_count = len(rows)

    ranked_categories = sorted(
        frequencies.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    distribution = []

    cumulative_percentage = 0.0

    for rank, (category, count) in enumerate(
        ranked_categories,
        start=1,
    ):
        percentage = (
            count / total_count
        ) * 100

        cumulative_percentage += percentage

        distribution.append(
            {
                "rank": rank,
                "category": category,
                "count": count,
                "percentage": percentage,
                "cumulative_percentage": (
                    cumulative_percentage
                ),
            }
        )

    top_category = distribution[0]

    summary = (
        f"{top_category['category']} is the most "
        f"frequent {dimension} category with "
        f"{top_category['count']} records."
    )

    return AnalysisEvidence(
        tool_name="frequency_analysis",
        summary=summary,
        data={
            "dimension": dimension,
            "total_count": total_count,
            "unique_categories": len(distribution),
            "distribution": distribution,
        },
        source_columns=[dimension],
        row_count=len(rows),
    )