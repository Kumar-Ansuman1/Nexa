from pydantic import BaseModel, Field


class AnalysisToolSelection(BaseModel):
    """
    Represents the analysis tools selected by JEV
    for an analytical user query.
    """

    tool_names: list[str] = Field(
        min_length=1,
        description=(
            "Names of the analysis tools selected by JEV."
        ),
    )