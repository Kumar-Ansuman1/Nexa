from src.query.sql.sql_executor import execute_sql
from src.query.state import NexaQueryState


def execute_sql_node(
    state: NexaQueryState,
) -> dict:
    """
    Execute the SQL query that has already passed validation.

    This node only executes validated SQL. It never executes the
    generated SQL directly.
    """

    validated_sql = state["validated_sql"]

    rows = execute_sql(
        sql=validated_sql,
    )

    columns = []

    if rows:
        columns = list(rows[0].keys())

    return {
        "rows": rows,
        "columns": columns,
        "status": "sql_executed",
        "error": None,
    }