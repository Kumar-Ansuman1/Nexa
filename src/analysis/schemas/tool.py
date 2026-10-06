from pydantic import BaseModel, Field


class AnalysisTool(BaseModel):
    """
    Contract describing an analysis tool available to NEXA.

    The metadata is used by JEV to understand which tool
    should be selected for a user's analytical question.
    """

    name: str = Field(
        min_length=1,
        description="Unique name of the analysis tool.",
    )

    description: str = Field(
        min_length=1,
        description="Description of what the tool does.",
    )

    required_semantics: list[str] = Field(
        default_factory=list,
        description=(
            "Semantic concepts required by the tool, "
            "such as metric or dimension."
        ),
    )

    argument_schema: dict = Field(
        default_factory=dict,
        description=(
            "Schema describing the arguments required "
            "when executing the tool."
        ),
    )

    evidence_type: str = Field(
        min_length=1,
        description=(
            "Name of the structured evidence type "
            "returned by the tool."
        ),
    )