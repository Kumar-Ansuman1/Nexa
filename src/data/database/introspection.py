"""
NEXA Database Introspection

Reads the actual user-data tables and columns from the SQLite database.
"""

from collections.abc import Iterable

from src.data.database.connection import get_connection


# These are NEXA's internal metadata tables.
# They are not user datasets and should not be exposed
# to the SQL generation layer.
METADATA_TABLES = {
    "datasets",
    "columns",
    "relationships",
    "semantic_embeddings",
}


def get_database_schema(
    dataset_names: Iterable[str] | None = None,
) -> str:
    """
    Build the database schema from the actual SQLite database.

    Parameters
    ----------
    dataset_names:
        Optional dataset names from the semantic registry.
        When provided, only those tables are included.

    Returns
    -------
    str
        Schema representation expected by the SQL generator
        and SQL validator.
    """

    connection = get_connection()

    try:
        available_tables = {
            row[0]
            for row in connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                  AND name NOT LIKE 'sqlite_%'
                ORDER BY name
                """
            ).fetchall()
        }

        if dataset_names is None:
            tables = sorted(
                available_tables - METADATA_TABLES
            )
        else:
            tables = []

            for dataset_name in dataset_names:
                if dataset_name in METADATA_TABLES:
                    continue

                if dataset_name not in available_tables:
                    raise ValueError(
                        f"Dataset table '{dataset_name}' "
                        "does not exist in the SQLite database."
                    )

                tables.append(dataset_name)

            tables = sorted(set(tables))

        if not tables:
            raise ValueError(
                "No user dataset tables were found in the SQLite database."
            )

        schema_parts: list[str] = []

        for table_name in tables:
            columns = connection.execute(
                f'PRAGMA table_info("{table_name}")'
            ).fetchall()

            if not columns:
                raise ValueError(
                    f"Dataset table '{table_name}' has no columns."
                )

            schema_parts.append(
                f"{table_name}:\n"
                + "\n".join(
                    f"    {column[1]}"
                    for column in columns
                )
            )

        return "\n\n".join(schema_parts)

    finally:
        connection.close()