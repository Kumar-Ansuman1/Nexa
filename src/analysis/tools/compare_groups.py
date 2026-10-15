from typing import Annotated, Any

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.analysis.schemas.evidence import AnalysisEvidence


@tool
def compare_groups(
    rows: Annotated[list[dict[str, Any]], InjectedState("rows")],
    metric: str,
    dimension: str,
    groups: list[Any] | None = None,
) -> AnalysisEvidence:
    """
    Compare groups using a numeric metric.

    The rows are injected from the analysis graph state.
    The LLM supplies metric, dimension, and optionally groups.

    Example:
        Compare revenue between India and the United States
        using metric="revenue", dimension="country",
        groups=["India", "United States"].
    """

    if not isinstance(rows, list):
        raise TypeError("rows must be a list.")

    if not rows:
        raise ValueError(
            "Cannot compare groups from empty result rows."
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

    if groups is not None:
        if not isinstance(groups, list):
            raise TypeError(
                "groups must be a list or None."
            )

        if len(groups) < 2:
            raise ValueError(
                "At least two groups are required for comparison."
            )

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

        if isinstance(row[metric], bool) or not isinstance(
            row[metric], (int, float)
        ):
            raise TypeError(
                f"Metric column '{metric}' must contain "
                "numeric values."
            )

    if groups is None:
        selected_rows = rows
    else:
        selected_rows = [
            row for row in rows
            if row[dimension] in groups
        ]

    if not selected_rows:
        raise ValueError(
            "None of the requested groups were found "
            "in the query result."
        )

    found_groups = {
        row[dimension]
        for row in selected_rows
    }

    if groups is not None:
        missing_groups = [
            group for group in groups
            if group not in found_groups
        ]

        if missing_groups:
            raise ValueError(
                "Requested groups were not found in the "
                f"query result: {missing_groups}"
            )

    values = [
        {
            "group": row[dimension],
            "value": row[metric],
        }
        for row in selected_rows
    ]

    values.sort(
        key=lambda item: item["value"],
        reverse=True,
    )

    highest = values[0]
    lowest = values[-1]

    difference = highest["value"] - lowest["value"]

    percentage_difference = None

    if lowest["value"] != 0:
        percentage_difference = (
            difference / abs(lowest["value"])
        ) * 100

    summary = (
        f"{highest['group']} has the highest {metric} "
        f"at {highest['value']}, compared with "
        f"{lowest['group']} at {lowest['value']}."
    )

    return AnalysisEvidence(
        tool_name="compare_groups",
        summary=summary,
        data={
            "metric": metric,
            "dimension": dimension,
            "groups": values,
            "highest": highest,
            "lowest": lowest,
            "difference": difference,
            "percentage_difference": percentage_difference,
        },
        source_columns=[
            dimension,
            metric,
        ],
        row_count=len(rows),
    )