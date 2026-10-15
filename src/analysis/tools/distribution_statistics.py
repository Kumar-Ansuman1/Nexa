from statistics import pvariance, pstdev
from typing import Annotated, Any

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from pydantic import BaseModel, ConfigDict, Field

from src.analysis.schemas.evidence import AnalysisEvidence


class DistributionStatisticsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metric: str = Field(
        description="The numeric column to analyze."
    )


def _percentile(
    values: list[int | float],
    percentile: float,
) -> float:
    if not 0 <= percentile <= 100:
        raise ValueError("percentile must be between 0 and 100.")

    sorted_values = sorted(values)
    position = (len(sorted_values) - 1) * percentile / 100

    lower_index = int(position)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    fraction = position - lower_index

    lower_value = sorted_values[lower_index]
    upper_value = sorted_values[upper_index]

    return lower_value + (upper_value - lower_value) * fraction


@tool
def distribution_statistics(
    metric: str,
    rows: Annotated[list[dict[str, Any]], InjectedState("rows")],
) -> AnalysisEvidence:
    """Calculate variance, standard deviation, range, quartiles, and percentiles for a numeric column."""

    if not isinstance(rows, list) or not rows:
        raise ValueError("rows must be a non-empty list.")

    if not isinstance(metric, str) or not metric.strip():
        raise ValueError("metric must be a non-empty column name.")

    values: list[int | float] = []

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"Row at index {index} must be a dictionary.")

        if metric not in row:
            raise ValueError(
                f"Metric column '{metric}' is missing from row {index}."
            )

        value = row[metric]

        if value is None:
            raise ValueError(
                f"Metric column '{metric}' contains a null value at row {index}."
            )

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(
                f"Metric column '{metric}' must contain only numeric values."
            )

        values.append(value)

    minimum = min(values)
    maximum = max(values)
    q1 = _percentile(values, 25)
    q3 = _percentile(values, 75)
    value_range = maximum - minimum
    iqr = q3 - q1
    variance = pvariance(values)
    standard_deviation = pstdev(values)
    percentile_10 = _percentile(values, 10)
    percentile_90 = _percentile(values, 90)

    return AnalysisEvidence(
        tool_name="distribution_statistics",
        summary=(
            f"{metric} has a standard deviation of {standard_deviation}, "
            f"a range of {value_range}, and an interquartile range of {iqr}."
        ),
        data={
            "metric": metric,
            "variance": variance,
            "standard_deviation": standard_deviation,
            "minimum": minimum,
            "maximum": maximum,
            "range": value_range,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "percentile_10": percentile_10,
            "percentile_90": percentile_90,
        },
        source_columns=[metric],
        row_count=len(rows),
    )
