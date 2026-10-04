"""
NEXA Query Pipeline

Orchestrates the complete flow from a natural-language question
to validated SQL and, optionally, actual database execution.

Pipeline:

    Natural-language question
        ↓
    Semantic Retrieval / JEV
        ↓
    Semantic Resolution
        ↓
    Query Planning
        ↓
    Join Planning
        ↓
    Execution Planning
        ↓
    SQL Generation
        ↓
    SQL Validation
        ↓
    SQL Execution
"""

import time
from typing import Any

from src.data.database.introspection import get_database_schema
from src.data.database.repositories.registry import load_registry
from src.data.semantic.catalog.catalog import (
    SemanticCatalogEntry,
    build_semantic_catalog,
)
from src.llm.schemas.registry import SemanticRegistry
from src.query.planning.execution_planner import build_execution_plan
from src.query.planning.join_planner import build_join_plan
from src.query.planning.query_planner import build_query_plan
from src.query.resolution.jev_resolution import resolve_query_semantics
from src.query.resolution.query_resolver import resolve_query
from src.query.sql.sql_executor import execute_sql
from src.query.sql.sql_generator import generate_sql
from src.query.sql.sql_validator import validate_sql


def _print_stage_time(
    stage_name: str,
    start_time: float,
) -> float:
    """
    Calculate and print the elapsed time for a pipeline stage.
    """

    elapsed = time.perf_counter() - start_time

    print(
        f"[TIMING] {stage_name:<35} "
        f"{elapsed:>10.3f} seconds",
        flush=True,
    )

    return elapsed


def run_query(
    query: str,
    registry: SemanticRegistry | None = None,
    catalog: list[SemanticCatalogEntry] | None = None,
    database_schema: str | None = None,
    execute: bool = False,
) -> str | list[dict[str, Any]]:
    """
    Run a natural-language query through the complete NEXA
    query pipeline.

    Parameters
    ----------
    query:
        User's natural-language question.

    registry:
        Optional semantic registry.

        If omitted, the approved registry is loaded
        from the SQLite database.

    catalog:
        Optional semantic catalog.

        If omitted, the catalog is built from the loaded
        semantic registry.

    database_schema:
        Optional database schema.

        If omitted, the schema is generated from the actual
        SQLite dataset tables.

    execute:
        If False, return validated SQL.

        If True, execute the validated SQL and return the
        actual database result.

    Returns
    -------
    str
        Validated SQL when execute=False.

    list[dict[str, Any]]
        Actual database result when execute=True.
    """

    pipeline_start = time.perf_counter()

    print(
        "\n[NEXA] Query pipeline started",
        flush=True,
    )

    print(
        "-" * 70,
        flush=True,
    )

    # =========================================================
    # 0. Input validation
    # =========================================================

    stage_start = time.perf_counter()

    if not isinstance(query, str):
        raise TypeError("query must be a string.")

    query = query.strip()

    if not query:
        raise ValueError(
            "Natural-language query must not be empty."
        )

    _print_stage_time(
        "Input validation",
        stage_start,
    )

    # =========================================================
    # 1. Load semantic registry
    # =========================================================

    stage_start = time.perf_counter()

    if registry is None:
        registry = load_registry()

    if not registry.datasets:
        raise ValueError(
            "No datasets are available in the semantic registry."
        )

    _print_stage_time(
        "Registry loading",
        stage_start,
    )

    # =========================================================
    # 2. Build semantic catalog
    # =========================================================

    stage_start = time.perf_counter()

    if catalog is None:
        catalog = build_semantic_catalog(
            registry=registry,
        )

    if not catalog:
        raise ValueError(
            "Semantic catalog is empty. "
            "Ensure approved semantic interpretations "
            "have been persisted."
        )

    _print_stage_time(
        "Catalog building",
        stage_start,
    )

    # =========================================================
    # 3. Database schema introspection
    # =========================================================

    stage_start = time.perf_counter()

    if database_schema is None:
        database_schema = get_database_schema(
            dataset_names=[
                dataset.dataset_name
                for dataset in registry.datasets
            ],
        )

    _print_stage_time(
        "Database schema introspection",
        stage_start,
    )

    # =========================================================
    # 4. Query Understanding
    # 5. Semantic Retrieval
    # 6. JEV Selection
    #
    # These are currently implemented together inside
    # resolve_query_semantics().
    # =========================================================

    stage_start = time.perf_counter()

    semantic_query = resolve_query_semantics(
        query=query,
        catalog=catalog,
    )

    _print_stage_time(
        "Query understanding / retrieval / JEV",
        stage_start,
    )

    # =========================================================
    # 7. Semantic Resolution
    # =========================================================

    stage_start = time.perf_counter()

    resolved_query = resolve_query(
        semantic_query=semantic_query,
        registry=registry,
    )

    _print_stage_time(
        "Semantic resolution",
        stage_start,
    )

    # =========================================================
    # 8. Query Planning
    # =========================================================

    stage_start = time.perf_counter()

    query_plan = build_query_plan(
        semantic_query=semantic_query,
        resolved_query=resolved_query,
    )

    _print_stage_time(
        "Query planning",
        stage_start,
    )

    # =========================================================
    # 9. Join Planning
    # =========================================================

    stage_start = time.perf_counter()

    join_plan = build_join_plan(
        query_plan=query_plan,
        registry=registry,
    )

    _print_stage_time(
        "Join planning",
        stage_start,
    )

    # =========================================================
    # 10. Execution Planning
    # =========================================================

    stage_start = time.perf_counter()

    execution_plan = build_execution_plan(
        query_plan=query_plan,
        join_plan=join_plan,
    )

    _print_stage_time(
        "Execution planning",
        stage_start,
    )

    # =========================================================
    # 11. SQL Generation
    # =========================================================

    stage_start = time.perf_counter()

    sql_result = generate_sql(
        execution_plan=execution_plan.model_dump(),
        database_schema=database_schema,
    )

    sql = sql_result.sql

    _print_stage_time(
        "SQL generation",
        stage_start,
    )

    # =========================================================
    # 12. SQL Validation
    # =========================================================

    stage_start = time.perf_counter()

    validated_sql = validate_sql(
        sql=sql,
        database_schema=database_schema,
        execution_plan=execution_plan,
    )

    _print_stage_time(
        "SQL validation",
        stage_start,
    )

    # =========================================================
    # Total pipeline time
    # =========================================================

    total_pipeline_time = (
        time.perf_counter() - pipeline_start
    )

    print(
        "-" * 70,
        flush=True,
    )

    print(
        f"[TIMING] TOTAL QUERY PIPELINE"
        f"{total_pipeline_time:>10.3f} seconds",
        flush=True,
    )

    print(
        "-" * 70,
        flush=True,
    )

    # =========================================================
    # 13. Optional SQL execution
    # =========================================================

    if execute:
        execution_start = time.perf_counter()

        result = execute_sql(validated_sql)

        execution_time = (
            time.perf_counter() - execution_start
        )

        print(
            f"[TIMING] SQL execution"
            f"{execution_time:>10.3f} seconds",
            flush=True,
        )

        return result

    return validated_sql