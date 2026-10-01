from pydantic import BaseModel, Field


class SemanticCandidate(BaseModel):
    semantic_id: str
    approved_meaning: str
    similarity: float = Field(ge=-1, le=1)