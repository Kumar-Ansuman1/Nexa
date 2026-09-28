from datetime import datetime, timezone
import json
from src.data.database.connection import get_connection
from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
)


def save_column(
    column: ColumnRegistryEntry,
    dataset_id: int,
) -> int:

    connection = get_connection()

    now = datetime.now(timezone.utc).isoformat()

    cursor = connection.execute(
        """
        INSERT INTO columns (
            dataset_id,
            source_column,
            suggested_meaning,
            suggested_description,
            suggested_role,
            confidence,
            evidence,
            approved_meaning,
            approved_description,
            approved_role,
            approval_status,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dataset_id,
            column.source_column,
            column.suggested_meaning,
            column.suggested_description,
            column.suggested_role,
            column.confidence,
            json.dumps(column.evidence),
            column.approved_meaning,
            column.approved_description,
            column.approved_role,
            column.approval_status.value,
            now,
            now,
        ),
    )

    connection.commit()

    column_id = cursor.lastrowid

    connection.close()

    return column_id

def get_columns(dataset_id: int) -> list[ColumnRegistryEntry]:
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            source_column,
            suggested_meaning,
            suggested_description,
            suggested_role,
            confidence,
            evidence,
            approved_meaning,
            approved_description,
            approved_role,
            approval_status
        FROM columns
        WHERE dataset_id = ?
        ORDER BY id
        """,
        (dataset_id,),
    ).fetchall()

    connection.close()

    return [
        ColumnRegistryEntry(
            source_column=row[0],
            suggested_meaning=row[1],
            suggested_description=row[2],
            suggested_role=row[3],
            confidence=row[4],
            evidence=json.loads(row[5]),
            approved_meaning=row[6],
            approved_description=row[7],
            approved_role=row[8],
            approval_status=ApprovalStatus(row[9]),
        )
        for row in rows
    ]

def get_column_id(
    dataset_name: str,
    source_column: str,
) -> tuple[int, int] | None:
    connection = get_connection()

    row = connection.execute(
        """
        SELECT
            d.id,
            c.id
        FROM datasets d
        JOIN columns c
            ON c.dataset_id = d.id
        WHERE d.dataset_name = ?
          AND c.source_column = ?
        """,
        (dataset_name, source_column),
    ).fetchone()

    connection.close()

    return row if row else None