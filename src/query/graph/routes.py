from src.query.state import NexaQueryState


MAX_SQL_VALIDATION_ATTEMPTS = 3


def route_after_sql_validation(
    state: NexaQueryState,
) -> str:
    """
    Decide the next step after SQL validation.

    Valid SQL proceeds to execution.

    Invalid SQL is sent back to SQL generation while the
    retry limit has not been reached.

    Once the retry limit is reached, the workflow fails.
    """

    status = state.get("status")
    attempts = state.get(
        "sql_validation_attempts",
        0,
    )

    if status == "sql_valid":
        return "execute_sql"

    if status == "sql_invalid":
        if attempts < MAX_SQL_VALIDATION_ATTEMPTS:
            return "generate_sql"

        return "sql_validation_failed"

    raise ValueError(
        f"Unexpected SQL validation status: {status}"
    )