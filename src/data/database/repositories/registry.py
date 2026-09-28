from src.data.database.repositories.columns import (
    get_column_id,
    save_column,
)
from src.data.database.repositories.datasets import save_dataset
from src.data.database.repositories.relationships import save_relationship
from src.llm.schemas.registry import SemanticRegistry
from src.data.database.repositories.datasets import get_dataset
from src.data.database.repositories.relationships import get_relationships
from src.llm.schemas.registry import SemanticRegistry
from src.data.database.connection import get_connection


def save_registry(registry: SemanticRegistry) -> None:
    dataset_ids = {}

    for dataset in registry.datasets:
        dataset_id = save_dataset(dataset)

        dataset_ids[dataset.dataset_name] = dataset_id

        for column in dataset.columns:
            save_column(
                column=column,
                dataset_id=dataset_id,
            )

    for relationship in registry.relationships:
        source = get_column_id(
            dataset_name=relationship.source_dataset,
            source_column=relationship.source_column,
        )

        target = get_column_id(
            dataset_name=relationship.target_dataset,
            source_column=relationship.target_column,
        )

        if source is None or target is None:
            raise ValueError(
                "Could not find one or both relationship columns."
            )

        source_dataset_id, source_column_id = source
        target_dataset_id, target_column_id = target

        save_relationship(
            relationship=relationship,
            source_dataset_id=source_dataset_id,
            source_column_id=source_column_id,
            target_dataset_id=target_dataset_id,
            target_column_id=target_column_id,
        )

def load_registry() -> SemanticRegistry:
    connection = get_connection()

    dataset_ids = connection.execute(
        """
        SELECT id
        FROM datasets
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    datasets = []

    for (dataset_id,) in dataset_ids:
        dataset = get_dataset(dataset_id)

        if dataset is not None:
            datasets.append(dataset)

    relationships = get_relationships()

    return SemanticRegistry(
        datasets=datasets,
        relationships=relationships,
    )