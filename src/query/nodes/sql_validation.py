from src.query.sql.sql_validator import (
    SQLValidationError,
    validate_sql,
)
from src.query.state import NexaQueryState


def validate_sql_node(
    state: NexaQueryState,
) -> dict:
    """
    Validate the generated SQL against the database schema
    and NEXA execution plan.

    Validation failures are stored in workflow state so the
    graph can route the query back to SQL generation.
    """

    generated_sql = state["generated_sql"]
    database_schema = state["database_schema"]
    execution_plan = state["execution_plan"]

    attempts = state.get(
        "sql_validation_attempts",
        0,
    )

    try:
        validated_sql = validate_sql(
            sql=generated_sql,
            database_schema=database_schema,
            execution_plan=execution_plan,
        )

        return {
            "validated_sql": validated_sql,
            "sql_validation_attempts": attempts + 1,
            "status": "sql_valid",
            "error": None,
        }

    except SQLValidationError as exc:
        return {
            "validated_sql": "",
            "sql_validation_attempts": attempts + 1,
            "status": "sql_invalid",
            "error": str(exc),
        }