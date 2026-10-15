from typing import Annotated, Any

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.analysis.schemas.evidence import AnalysisEvidence


@tool
def frequency_analysis(
    rows: Annotated[list[dict[str, Any]], InjectedState("rows")],
    dimension: str,
) -> AnalysisEvidence:
    """
    Analyze how frequently each category occurs in the query results.

    Calculates counts, percentages, cumulative percentages, and
    frequency rankings for the requested dimension.

    Uses rows supplied through LangGraph state. Does not execute SQL,
    access the database, or call an LLM.
    """
    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot calculate frequency analysis from empty result rows."
        )

    if not isinstance(dimension, str) or not dimension.strip():
        raise ValueError("dimension must be a non-empty string.")

    dimension = dimension.strip()
    frequencies: dict[Any, int] = {}

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise TypeError(
                f"Row at index {index} must be a dictionary."
            )

        if dimension not in row:
            raise ValueError(
                f"Dimension column '{dimension}' is missing from row {index}."
            )

        category = row[dimension]

        if category is None:
            raise ValueError(
                f"Dimension column '{dimension}' contains NULL at row {index}."
            )

        try:
            frequencies[category] = frequencies.get(category, 0) + 1
        except TypeError as exc:
            raise TypeError(
                f"Category in dimension '{dimension}' at row {index} "
                "must be hashable."
            ) from exc

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
        percentage = (count / total_count) * 100
        cumulative_percentage += percentage

        distribution.append(
            {
                "rank": rank,
                "category": category,
                "count": count,
                "percentage": percentage,
                "cumulative_percentage": cumulative_percentage,
            }
        )

    # Avoid floating-point accumulation artifacts in the final percentage.
    distribution[-1]["cumulative_percentage"] = 100.0

    top_category = distribution[0]

    summary = (
        f"{top_category['category']} is the most frequent "
        f"{dimension} category with {top_category['count']} records."
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
        row_count=total_count,
    )
