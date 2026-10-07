from src.query.sql.sql_generator import generate_sql
from src.query.state import NexaQueryState


def generate_sql_node(
    state: NexaQueryState,
) -> dict:
    """
    Generate SQL from the execution plan and database schema.

    If the previous SQL attempt failed validation, the previous SQL
    and validation error are passed to the generator so it can
    produce a corrected query.
    """

    execution_plan = state["execution_plan"]
    database_schema = state["database_schema"]

    previous_sql = state.get("generated_sql")
    validation_error = state.get("error")

    sql_result = generate_sql(
        execution_plan=execution_plan.model_dump(),
        database_schema=database_schema,
        previous_sql=previous_sql,
        validation_error=validation_error,
    )

    return {
        "generated_sql": sql_result.sql,
        "status": "sql_generated",
    }   