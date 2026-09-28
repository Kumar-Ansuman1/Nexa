from datetime import datetime, timezone
from src.data.database.repositories.columns import get_columns
from src.data.database.connection import get_connection
from src.llm.schemas.registry import DatasetRegistryEntry


def save_dataset(dataset: DatasetRegistryEntry) -> int:
    connection = get_connection()

    now = datetime.now(timezone.utc).isoformat()

    cursor = connection.execute(
        """
        INSERT INTO datasets (
            dataset_name,
            suggested_name,
            suggested_description,
            confidence,
            approved_name,
            approved_description,
            approval_status,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dataset.dataset_name,
            dataset.suggested_name,
            dataset.suggested_description,
            dataset.confidence,
            dataset.approved_name,
            dataset.approved_description,
            dataset.approval_status.value,
            now,
            now,
        ),
    )

    connection.commit()

    dataset_id = cursor.lastrowid

    connection.close()

    return dataset_id

from src.llm.schemas.registry import DatasetRegistryEntry


def get_dataset(dataset_id: int) -> DatasetRegistryEntry | None:
    connection = get_connection()

    row = connection.execute(
        """
        SELECT
            dataset_name,
            suggested_name,
            suggested_description,
            confidence,
            approved_name,
            approved_description,
            approval_status
        FROM datasets
        WHERE id = ?
        """,
        (dataset_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return DatasetRegistryEntry(
        dataset_name=row[0],
        suggested_name=row[1],
        suggested_description=row[2],
        confidence=row[3],
        approved_name=row[4],
        approved_description=row[5],
        approval_status=row[6],
        columns=get_columns(dataset_id),
    )