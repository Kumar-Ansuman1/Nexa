from pydantic import BaseModel

from src.llm.schemas.registry import (
    ApprovalStatus,
    SemanticRegistry,
)


class SemanticCatalogEntry(BaseModel):
    semantic_id: str
    approved_meaning: str


def build_semantic_catalog(
    registry: SemanticRegistry,
) -> list[SemanticCatalogEntry]:

    catalog = []

    for dataset in registry.datasets:
        for column in dataset.columns:

            if (
                column.approval_status == ApprovalStatus.APPROVED
                and column.approved_meaning
            ):
                catalog.append(
                    SemanticCatalogEntry(
                        semantic_id=column.semantic_id,
                        approved_meaning=column.approved_meaning,
                    )
                )

    return catalog