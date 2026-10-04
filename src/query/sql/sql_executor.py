"""
NEXA SQL Executor

Executes validated read-only SQL against the NEXA SQLite database.
"""

from typing import Any

from src.data.database.connection import get_connection


def execute_sql(
    sql: str,
) -> list[dict[str, Any]]:
    """
    Execute validated SQL against the NEXA SQLite database.

    Parameters
    ----------
    sql:
        SQL query that has already passed NEXA validation.

    Returns
    -------
    list[dict[str, Any]]
        Query results represented as dictionaries.
    """

    if not isinstance(sql, str):
        raise TypeError("sql must be a string.")

    sql = sql.strip()

    if not sql:
        raise ValueError("SQL query must not be empty.")

    connection = get_connection()

    try:
        cursor = connection.execute(sql)

        columns = [
            description[0]
            for description in cursor.description
        ]

        rows = cursor.fetchall()

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    finally:
        connection.close()