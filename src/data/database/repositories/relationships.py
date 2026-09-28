import json
from datetime import datetime, timezone

from src.data.database.connection import get_connection
from src.llm.schemas.registry import RelationshipRegistryEntry,ApprovalStatus


def save_relationship(
    relationship: RelationshipRegistryEntry,
    source_dataset_id: int,
    source_column_id: int,
    target_dataset_id: int,
    target_column_id: int,
) -> int:

    connection = get_connection()

    now = datetime.now(timezone.utc).isoformat()

    cursor = connection.execute(
        """
        INSERT INTO relationships (
            source_dataset_id,
            source_column_id,
            target_dataset_id,
            target_column_id,
            relationship_type,
            confidence,
            evidence,
            approval_status,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            source_dataset_id,
            source_column_id,
            target_dataset_id,
            target_column_id,
            relationship.relationship_type,
            relationship.confidence,
            json.dumps(relationship.evidence),
            relationship.approval_status.value,
            now,
            now,
        ),
    )

    connection.commit()

    relationship_id = cursor.lastrowid

    connection.close()

    return relationship_id

def get_relationships() -> list[RelationshipRegistryEntry]:
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            d1.dataset_name,
            c1.source_column,
            d2.dataset_name,
            c2.source_column,
            r.relationship_type,
            r.confidence,
            r.evidence,
            r.approval_status
        FROM relationships r
        JOIN datasets d1
            ON r.source_dataset_id = d1.id
        JOIN columns c1
            ON r.source_column_id = c1.id
        JOIN datasets d2
            ON r.target_dataset_id = d2.id
        JOIN columns c2
            ON r.target_column_id = c2.id
        ORDER BY r.id
        """
    ).fetchall()

    connection.close()

    return [
        RelationshipRegistryEntry(
            source_dataset=row[0],
            source_column=row[1],
            target_dataset=row[2],
            target_column=row[3],
            relationship_type=row[4],
            confidence=row[5],
            evidence=json.loads(row[6]),
            approval_status=ApprovalStatus(row[7]),
        )
        for row in rows
    ]