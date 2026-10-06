from typing import Any

from pydantic import BaseModel, Field


class AnalysisEvidence(BaseModel):
    """
    Structured evidence produced by a deterministic
    analysis tool.

    This represents facts calculated from the actual
    query result returned by the Query Pipeline.
    """

    tool_name: str = Field(
        min_length=1,
        description="Name of the tool that produced the evidence.",
    )

    summary: str = Field(
        min_length=1,
        description="Short factual description of the analysis result.",
    )

    data: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Structured analytical facts produced by the tool."
        ),
    )

    source_columns: list[str] = Field(
        default_factory=list,
        description=(
            "Columns from the query result used by the analysis."
        ),
    )

    row_count: int = Field(
        ge=0,
        description="Number of input rows used by the tool.",
    )