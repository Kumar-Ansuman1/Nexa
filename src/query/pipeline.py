"""
NEXA Query Pipeline

Orchestrates the complete flow from a natural-language question
to a generated SQL query.

SQL execution is intentionally NOT handled here.
"""

from src.data.semantic.catalog.catalog import SemanticCatalogEntry
from src.llm.schemas.registry import SemanticRegistry
from src.query.resolution.jev_resolution import resolve_query_semantics
from src.query.resolution.query_resolver import resolve_query
from src.query.planning.query_planner import build_query_plan
from src.query.planning.join_planner import build_join_plan
from src.query.planning.execution_planner import build_execution_plan
from src.query.sql.sql_generator import generate_sql
from src.query.sql.sql_validator import validate_sql


def run_query(
    query: str,
    registry: SemanticRegistry,
    catalog: list[SemanticCatalogEntry],
    database_schema: str,
) -> str:
    """
    Convert a natural-language query into SQL.

    Parameters
    ----------
    query:
        User's natural-language question.

    registry:
        NEXA semantic registry.

    catalog:
        Semantic catalog used for retrieval.

    database_schema:
        Database schema supplied to the SQL generator.

    Returns
    -------
    str
        Generated SQL query.

    Notes
    -----
    This function does not execute SQL.
    SQL validation is performed before the SQL is returned.
    """

    # ---------------------------------------------------------
    # 1. Query Understanding
    # 2. Semantic Retrieval
    # 3. JEV Selection
    # ---------------------------------------------------------
    #
    # These three stages are currently combined inside
    # resolve_query_semantics().
    #
    semantic_query = resolve_query_semantics(
        query=query,
        catalog=catalog,
    )

    # ---------------------------------------------------------
    # 4. Semantic Resolution
    # ---------------------------------------------------------
    #
    # Convert selected semantic IDs into actual
    # dataset + source-column references.
    #
    resolved_query = resolve_query(
        semantic_query=semantic_query,
        registry=registry,
    )

    # ---------------------------------------------------------
    # 5. Query Planning
    # ---------------------------------------------------------
    #
    # Build a logical query plan from the resolved semantics.
    #
    query_plan = build_query_plan(
        semantic_query=semantic_query,
        resolved_query=resolved_query,
    )

    # ---------------------------------------------------------
    # 6. Join Planning
    # ---------------------------------------------------------
    #
    # Determine the joins required between datasets.
    #
    join_plan = build_join_plan(
        query_plan=query_plan,
        registry=registry,
    )

    # ---------------------------------------------------------
    # 7. Execution Planning
    # ---------------------------------------------------------
    #
    # Combine the query plan and join plan into the
    # execution plan consumed by SQL generation.
    #
    execution_plan = build_execution_plan(
        query_plan=query_plan,
        join_plan=join_plan,
    )

    # ---------------------------------------------------------
    # 8. SQL Generation
    # ---------------------------------------------------------
    #
    # SQL generation currently expects a dictionary,
    # so convert the Pydantic execution plan to a dict.
    #
    sql_result = generate_sql(
        execution_plan=execution_plan.model_dump(),
        database_schema=database_schema,
    )

    sql = sql_result.sql

    # ---------------------------------------------------------
    # 9. SQL Validation
    # ---------------------------------------------------------

    validated_sql = validate_sql(
    sql=sql,
    database_schema=database_schema,
    execution_plan=execution_plan,
    )

    return validated_sql