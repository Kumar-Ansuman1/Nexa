from pydantic import BaseModel, Field

class DatasetInterpretation(BaseModel):
    suggested_name: str
    description: str
    confidence: float = Field(ge=0, le=1)


class SemanticSuggestion(BaseModel):
    source_column: str
    suggested_meaning: str
    description: str
    role: str
    confidence: float = Field(ge=0, le=1)
    evidence: list[str]

class SemanticMapping(BaseModel):
    dataset: DatasetInterpretation
    columns: list[SemanticSuggestion]