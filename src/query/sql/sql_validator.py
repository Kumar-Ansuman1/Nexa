"""
NEXA SQL Validator

Validates generated SQL against:

1. Basic SQL safety rules
2. The supplied database schema
3. The NEXA execution plan

The validator does not execute SQL.
"""

import re

from src.llm.schemas.execution_plan import ExecutionPlan


class SQLValidationError(ValueError):
    """Raised when generated SQL fails validation."""


FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
    "MERGE",
    "GRANT",
    "REVOKE",
}


# =============================================================
# Public API
# =============================================================


def validate_sql(
    sql: str,
    database_schema: str,
    execution_plan: ExecutionPlan,
) -> str:
    """
    Validate generated SQL against the database schema
    and NEXA execution plan.

    Returns the SQL if validation succeeds.
    Raises SQLValidationError otherwise.

    SQL is never executed here.
    """

    # ---------------------------------------------------------
    # 1. Basic validation
    # ---------------------------------------------------------

    if not isinstance(sql, str):
        raise SQLValidationError(
            "Generated SQL must be a string."
        )

    sql = sql.strip()

    if not sql:
        raise SQLValidationError(
            "Generated SQL is empty."
        )

    sql_without_trailing_semicolon = (
        sql.rstrip(";").strip()
    )

    # ---------------------------------------------------------
    # 2. Single statement
    # ---------------------------------------------------------

    if ";" in sql_without_trailing_semicolon:
        raise SQLValidationError(
            "Multiple SQL statements are not allowed."
        )

    # ---------------------------------------------------------
    # 3. SELECT only
    # ---------------------------------------------------------

    first_keyword_match = re.match(
        r"^\s*([A-Za-z]+)",
        sql_without_trailing_semicolon,
    )

    if not first_keyword_match:
        raise SQLValidationError(
            "Unable to determine SQL statement type."
        )

    first_keyword = first_keyword_match.group(1).upper()

    if first_keyword != "SELECT":
        raise SQLValidationError(
            f"Only SELECT statements are allowed. "
            f"Found: {first_keyword}"
        )

    # ---------------------------------------------------------
    # 4. Forbidden keywords
    # ---------------------------------------------------------

    sql_upper = sql_without_trailing_semicolon.upper()

    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(
            rf"\b{re.escape(keyword)}\b",
            sql_upper,
        ):
            raise SQLValidationError(
                f"Forbidden SQL keyword detected: {keyword}"
            )

    # ---------------------------------------------------------
    # 5. Parse database schema
    # ---------------------------------------------------------

    schema_tables = _extract_schema_tables(
        database_schema
    )

    if not schema_tables:
        raise SQLValidationError(
            "Database schema does not contain any tables."
        )

    # ---------------------------------------------------------
    # 6. Validate referenced tables
    # ---------------------------------------------------------

    referenced_tables = _extract_referenced_tables(
        sql_without_trailing_semicolon
    )

    unknown_tables = (
        referenced_tables - schema_tables.keys()
    )

    if unknown_tables:
        raise SQLValidationError(
            "SQL references tables that are not present "
            "in the database schema: "
            f"{sorted(unknown_tables)}"
        )

    # ---------------------------------------------------------
    # 7. Extract table aliases
    # ---------------------------------------------------------

    aliases = _extract_table_aliases(
        sql_without_trailing_semicolon
    )

    # ---------------------------------------------------------
    # 8. Validate referenced columns
    # ---------------------------------------------------------

    referenced_columns = _extract_qualified_columns(
        sql_without_trailing_semicolon
    )

    for alias, column in referenced_columns:

        if alias not in aliases:
            raise SQLValidationError(
                f"SQL references unknown table alias: {alias}"
            )

        table = aliases[alias]

        table_columns = schema_tables.get(
            table,
            set(),
        )

        if column not in table_columns:
            raise SQLValidationError(
                f"Column '{table}.{column}' "
                "does not exist in the database schema."
            )

    # ---------------------------------------------------------
    # 9. Validate execution-plan datasets
    # ---------------------------------------------------------

    _validate_execution_plan_datasets(
        execution_plan=execution_plan,
        schema_tables=schema_tables,
    )

    # ---------------------------------------------------------
    # 10. Validate execution-plan columns
    # ---------------------------------------------------------

    _validate_execution_plan_columns(
        execution_plan=execution_plan,
        schema_tables=schema_tables,
    )

    # ---------------------------------------------------------
    # 11. Validate execution-plan joins
    # ---------------------------------------------------------

    _validate_execution_plan_joins(
        execution_plan=execution_plan,
        schema_tables=schema_tables,
    )

    # ---------------------------------------------------------
    # 12. Validate SQL against execution plan
    # ---------------------------------------------------------

    _validate_plan_usage(
        sql=sql_without_trailing_semicolon,
        execution_plan=execution_plan,
        aliases=aliases,
    )

    return sql


# =============================================================
# Schema Parsing
# =============================================================


def _extract_schema_tables(
    database_schema: str,
) -> dict[str, set[str]]:
    """
    Parse the simple NEXA schema representation.

    Example:

        customers:
            customer_id
            country

        transactions:
            customer_id
            revenue
            date
    """

    if not isinstance(database_schema, str):
        raise SQLValidationError(
            "Database schema must be a string."
        )

    tables: dict[str, set[str]] = {}

    current_table: str | None = None

    for raw_line in database_schema.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        table_match = re.match(
            r"^([A-Za-z_][A-Za-z0-9_]*)\s*:",
            line,
        )

        if table_match:

            current_table = (
                table_match.group(1).lower()
            )

            tables[current_table] = set()

            continue

        if current_table is not None:

            column_match = re.match(
                r"^([A-Za-z_][A-Za-z0-9_]*)$",
                line,
            )

            if column_match:

                tables[current_table].add(
                    column_match.group(1).lower()
                )

    return tables


# =============================================================
# SQL Parsing
# =============================================================


def _extract_referenced_tables(
    sql: str,
) -> set[str]:

    matches = re.findall(
        r"\b(?:FROM|JOIN)\s+"
        r"([A-Za-z_][A-Za-z0-9_]*)",
        sql,
        flags=re.IGNORECASE,
    )

    return {
        table.lower()
        for table in matches
    }


def _extract_table_aliases(
    sql: str,
) -> dict[str, str]:
    """
    Extract table names and aliases.

    Example:

        FROM customers c
        JOIN transactions t

    becomes:

        {
            "customers": "customers",
            "c": "customers",
            "transactions": "transactions",
            "t": "transactions",
        }

    Supports both:

        FROM customers c

    and:

        FROM customers AS c
    """

    aliases: dict[str, str] = {}

    # These tokens can appear immediately after a table
    # without actually being an alias.
    sql_keywords = {
        "ON",
        "JOIN",
        "INNER",
        "LEFT",
        "RIGHT",
        "FULL",
        "CROSS",
        "OUTER",
        "WHERE",
        "GROUP",
        "ORDER",
        "HAVING",
        "LIMIT",
        "OFFSET",
        "UNION",
        "EXCEPT",
        "INTERSECT",
    }

    sql_keywords = {
        keyword.lower()
        for keyword in sql_keywords
    }

    pattern = (
        r"\b(?:FROM|JOIN)\s+"
        r"([A-Za-z_][A-Za-z0-9_]*)"
        r"(?:\s+(?:AS\s+)?"
        r"([A-Za-z_][A-Za-z0-9_]*))?"
    )

    for match in re.finditer(
        pattern,
        sql,
        flags=re.IGNORECASE,
    ):

        table = match.group(1).lower()
        alias = match.group(2)

        # Always register the real table name.
        aliases[table] = table

        if alias:

            alias_lower = alias.lower()

            # Do not treat SQL keywords as aliases.
            if alias_lower not in sql_keywords:
                aliases[alias_lower] = table

    return aliases


def _extract_qualified_columns(
    sql: str,
) -> list[tuple[str, str]]:
    """
    Extract qualified references such as:

        c.country
        t.revenue
        c.customer_id
    """

    matches = re.findall(
        r"\b([A-Za-z_][A-Za-z0-9_]*)"
        r"\.([A-Za-z_][A-Za-z0-9_]*)\b",
        sql,
    )

    return [
        (
            alias.lower(),
            column.lower(),
        )
        for alias, column in matches
    ]


# =============================================================
# Execution Plan Validation
# =============================================================


def _validate_execution_plan_datasets(
    execution_plan: ExecutionPlan,
    schema_tables: dict[str, set[str]],
) -> None:

    query_plan = execution_plan.query_plan

    for dataset in query_plan.required_datasets:

        if dataset.lower() not in schema_tables:

            raise SQLValidationError(
                "Execution plan references dataset "
                f"'{dataset}' which is not present "
                "in the database schema."
            )


def _validate_execution_plan_columns(
    execution_plan: ExecutionPlan,
    schema_tables: dict[str, set[str]],
) -> None:

    query_plan = execution_plan.query_plan

    # ---------------------------------------------------------
    # Metric
    # ---------------------------------------------------------

    if query_plan.metric:

        _validate_plan_column(
            dataset=query_plan.metric.dataset,
            column=query_plan.metric.column,
            schema_tables=schema_tables,
        )

    # ---------------------------------------------------------
    # Dimensions
    # ---------------------------------------------------------

    for dimension in query_plan.dimensions:

        _validate_plan_column(
            dataset=dimension.dataset,
            column=dimension.column,
            schema_tables=schema_tables,
        )


def _validate_plan_column(
    dataset: str,
    column: str,
    schema_tables: dict[str, set[str]],
) -> None:

    dataset_lower = dataset.lower()
    column_lower = column.lower()

    if dataset_lower not in schema_tables:

        raise SQLValidationError(
            "Execution plan references unknown "
            f"dataset '{dataset}'."
        )

    if column_lower not in schema_tables[dataset_lower]:

        raise SQLValidationError(
            "Execution plan references unknown "
            f"column '{dataset}.{column}'."
        )


# =============================================================
# Join Validation
# =============================================================


def _validate_execution_plan_joins(
    execution_plan: ExecutionPlan,
    schema_tables: dict[str, set[str]],
) -> None:

    for join in execution_plan.join_plan.joins:

        _validate_plan_column(
            dataset=join.left_dataset,
            column=join.left_column,
            schema_tables=schema_tables,
        )

        _validate_plan_column(
            dataset=join.right_dataset,
            column=join.right_column,
            schema_tables=schema_tables,
        )


# =============================================================
# SQL ↔ Execution Plan Validation
# =============================================================


def _validate_plan_usage(
    sql: str,
    execution_plan: ExecutionPlan,
    aliases: dict[str, str],
) -> None:
    """
    Verify that the generated SQL actually implements
    the execution plan.

    This is intentionally deterministic.

    The validator does not ask an LLM whether the SQL
    looks correct.
    """

    query_plan = execution_plan.query_plan

    # ---------------------------------------------------------
    # Metric
    # ---------------------------------------------------------

    if query_plan.metric:

        expected_dataset = (
            query_plan.metric.dataset.lower()
        )

        expected_column = (
            query_plan.metric.column.lower()
        )

        expected_operation = (
            query_plan.operation.value.upper()
        )

        aggregate_expressions = (
            _extract_aggregate_expressions(sql)
        )

        metric_found = False

        for operation, alias, column in aggregate_expressions:

            if operation != expected_operation:
                continue

            resolved_dataset = aliases.get(
                alias.lower()
            )

            if resolved_dataset != expected_dataset:
                continue

            if column.lower() != expected_column:
                continue

            metric_found = True
            break

        if not metric_found:

            raise SQLValidationError(
                "Execution plan metric is not correctly "
                "represented in the generated SQL. "
                f"Expected "
                f"{expected_operation}"
                f"({expected_dataset}."
                f"{expected_column})."
            )

    # ---------------------------------------------------------
    # Dimensions
    # ---------------------------------------------------------

    for dimension in query_plan.dimensions:

        expected_dataset = (
            dimension.dataset.lower()
        )

        expected_column = (
            dimension.column.lower()
        )

        dimension_found = False

        for alias, column in _extract_qualified_columns(
            sql
        ):

            resolved_dataset = aliases.get(
                alias.lower()
            )

            if resolved_dataset != expected_dataset:
                continue

            if column.lower() != expected_column:
                continue

            dimension_found = True
            break

        if not dimension_found:

            raise SQLValidationError(
                "Execution plan dimension "
                f"'{dimension.dataset}."
                f"{dimension.column}' is not used "
                "in the generated SQL."
            )

    # ---------------------------------------------------------
    # Joins
    # ---------------------------------------------------------

    for join in execution_plan.join_plan.joins:

        if not _join_exists_in_sql(
            sql=sql,
            join=join,
            aliases=aliases,
        ):

            raise SQLValidationError(
                "Execution plan join is not represented "
                "in the generated SQL: "
                f"{join.left_dataset}."
                f"{join.left_column} = "
                f"{join.right_dataset}."
                f"{join.right_column}"
            )


# =============================================================
# Aggregate Parsing
# =============================================================


def _extract_aggregate_expressions(
    sql: str,
) -> list[tuple[str, str, str]]:
    """
    Extract simple aggregate expressions.

    Example:

        SUM(t.revenue)

    becomes:

        [
            ("SUM", "t", "revenue")
        ]

    Supported operations:

        SUM
        AVG
        COUNT
        MIN
        MAX
    """

    pattern = (
        r"\b(SUM|AVG|COUNT|MIN|MAX)"
        r"\s*\(\s*"
        r"([A-Za-z_][A-Za-z0-9_]*)"
        r"\."
        r"([A-Za-z_][A-Za-z0-9_]*)"
        r"\s*\)"
    )

    matches = re.findall(
        pattern,
        sql,
        flags=re.IGNORECASE,
    )

    return [
        (
            operation.upper(),
            alias.lower(),
            column.lower(),
        )
        for operation, alias, column in matches
    ]


# =============================================================
# Join SQL Validation
# =============================================================


def _join_exists_in_sql(
    sql: str,
    join,
    aliases: dict[str, str],
) -> bool:
    """
    Verify that the planned join exists as an actual
    equality condition in the generated SQL.

    Example:

        c.customer_id = t.customer_id
    """

    equality_pattern = (
        r"\b([A-Za-z_][A-Za-z0-9_]*)"
        r"\.([A-Za-z_][A-Za-z0-9_]*)"
        r"\s*=\s*"
        r"([A-Za-z_][A-Za-z0-9_]*)"
        r"\.([A-Za-z_][A-Za-z0-9_]*)\b"
    )

    matches = re.findall(
        equality_pattern,
        sql,
        flags=re.IGNORECASE,
    )

    expected_left = (
        join.left_dataset.lower(),
        join.left_column.lower(),
    )

    expected_right = (
        join.right_dataset.lower(),
        join.right_column.lower(),
    )

    for (
        left_alias,
        left_column,
        right_alias,
        right_column,
    ) in matches:

        left_dataset = aliases.get(
            left_alias.lower()
        )

        right_dataset = aliases.get(
            right_alias.lower()
        )

        actual_left = (
            left_dataset,
            left_column.lower(),
        )

        actual_right = (
            right_dataset,
            right_column.lower(),
        )

        # Planned direction.
        if (
            actual_left == expected_left
            and actual_right == expected_right
        ):
            return True

        # Reverse direction is also valid.
        if (
            actual_left == expected_right
            and actual_right == expected_left
        ):
            return True

    return False