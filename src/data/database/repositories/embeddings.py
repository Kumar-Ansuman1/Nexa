import json
from datetime import datetime, timezone

from src.data.database.connection import get_connection


def save_embedding(
    semantic_id: str,
    model_name: str,
    embedding: list[float],
) -> None:
    connection = get_connection()

    now = datetime.now(timezone.utc).isoformat()

    embedding_json = json.dumps(embedding)

    connection.execute(
        """
        INSERT INTO semantic_embeddings (
            semantic_id,
            model_name,
            embedding,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(semantic_id)
        DO UPDATE SET
            model_name = excluded.model_name,
            embedding = excluded.embedding,
            updated_at = excluded.updated_at
        """,
        (
            semantic_id,
            model_name,
            embedding_json,
            now,
            now,
        ),
    )

    connection.commit()
    connection.close()


def get_embedding(
    semantic_id: str,
) -> tuple[str, list[float]] | None:
    connection = get_connection()

    row = connection.execute(
        """
        SELECT model_name, embedding
        FROM semantic_embeddings
        WHERE semantic_id = ?
        """,
        (semantic_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    model_name, embedding_json = row

    return (
        model_name,
        json.loads(embedding_json),
    )


def get_all_embeddings() -> list[tuple[str, str, list[float]]]:
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT semantic_id, model_name, embedding
        FROM semantic_embeddings
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    return [
        (
            semantic_id,
            model_name,
            json.loads(embedding_json),
        )
        for semantic_id, model_name, embedding_json in rows
    ]


def delete_embedding(
    semantic_id: str,
) -> None:
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM semantic_embeddings
        WHERE semantic_id = ?
        """,
        (semantic_id,),
    )

    connection.commit()
    connection.close()