from enum import Enum
from pydantic import BaseModel, Field


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ColumnRegistryEntry(BaseModel):
    source_column: str

    suggested_meaning: str
    suggested_description: str
    suggested_role: str
    confidence: float = Field(ge=0, le=1)
    evidence: list[str]

    approved_meaning: str | None = None
    approved_description: str | None = None
    approved_role: str | None = None

    approval_status: ApprovalStatus = ApprovalStatus.PENDING

class DatasetRegistryEntry(BaseModel):
    dataset_name: str

    suggested_name: str
    suggested_description: str
    confidence: float = Field(ge=0, le=1)

    approved_name: str | None = None
    approved_description: str | None = None

    approval_status: ApprovalStatus = ApprovalStatus.PENDING

    columns: list[ColumnRegistryEntry]

class RelationshipRegistryEntry(BaseModel):
    source_dataset: str
    source_column: str

    target_dataset: str
    target_column: str

    relationship_type: str

    confidence: float = Field(ge=0, le=1)
    evidence: list[str]

    approval_status: ApprovalStatus = ApprovalStatus.PENDING

class SemanticRegistry(BaseModel):
    datasets: list[DatasetRegistryEntry]
    relationships: list[RelationshipRegistryEntry]