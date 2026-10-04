from src.data.database.repositories.embeddings import save_embedding
from src.embeddings.models.jina import embed_text
from src.llm.schemas.registry import (
    ApprovalStatus,
    SemanticRegistry,
)


EMBEDDING_MODEL = "jina-embeddings-v5-text-nano"


def generate_registry_embeddings(
    registry: SemanticRegistry,
) -> int:
    generated_count = 0

    for dataset in registry.datasets:
        for column in dataset.columns:

            if (
                column.approval_status != ApprovalStatus.APPROVED
                or not column.approved_meaning
            ):
                continue

            embedding = embed_text(
                column.approved_meaning
            )

            save_embedding(
                semantic_id=column.semantic_id,
                model_name=EMBEDDING_MODEL,
                embedding=embedding,
            )

            generated_count += 1

    return generated_count