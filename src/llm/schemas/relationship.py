from pydantic import BaseModel, Field


class RelationshipSignals(BaseModel):
    role_compatible: bool
    datatype_compatible: bool
    name_similarity: float = Field(ge=0, le=1)
    value_overlap: float = Field(ge=0, le=1)
    source_uniqueness: float = Field(ge=0, le=1)
    target_uniqueness: float = Field(ge=0, le=1)
    cardinality: str


class RelationshipCandidate(BaseModel):
    source_dataset: str
    source_column: str

    target_dataset: str
    target_column: str

    signals: RelationshipSignals

    candidate_score: float = Field(ge=0, le=1)


class RelationshipInterpretation(BaseModel):
    source_dataset: str
    source_column: str

    target_dataset: str
    target_column: str

    relationship_type: str

    confidence: float = Field(ge=0, le=1)

    evidence: list[str]