"""
Tests for NEXA SQL Validator.

Run from the project root:

    python -m tests.test_sql_validator
"""

from src.llm.schemas.execution_plan import ExecutionPlan
from src.llm.schemas.join_plan import JoinPlan, JoinStep
from src.llm.schemas.query import QueryOperation
from src.llm.schemas.query_plan import QueryPlan, ResolvedColumn

from src.query.sql.sql_validator import (
    SQLValidationError,
    validate_sql,
)


DATABASE_SCHEMA = """
customers:
    customer_id
    country

transactions:
    customer_id
    revenue
    date
"""


def create_execution_plan() -> ExecutionPlan:
    """
    Create a controlled execution plan for:

        Show the total revenue by country.
    """

    query_plan = QueryPlan(
        metric=ResolvedColumn(
            dataset="transactions",
            column="revenue",
        ),
        dimensions=[
            ResolvedColumn(
                dataset="customers",
                column="country",
            )
        ],
        operation=QueryOperation.SUM,
        required_datasets=[
            "transactions",
            "customers",
        ],
    )

    join_plan = JoinPlan(
        joins=[
            JoinStep(
                left_dataset="customers",
                left_column="customer_id",
                right_dataset="transactions",
                right_column="customer_id",
            )
        ]
    )

    return ExecutionPlan(
        query_plan=query_plan,
        join_plan=join_plan,
    )


def test_valid_sql():
    """Correct SQL should pass validation."""

    execution_plan = create_execution_plan()

    sql = """
    SELECT
        c.country,
        SUM(t.revenue) AS revenue_sum
    FROM customers c
    JOIN transactions t
        ON c.customer_id = t.customer_id
    GROUP BY c.country;
    """

    result = validate_sql(
        sql=sql,
        database_schema=DATABASE_SCHEMA,
        execution_plan=execution_plan,
    )

    assert result == sql.strip()

    print("PASS: valid SQL accepted")


def test_wrong_metric():
    """
    The SQL uses an existing column, but it is not the
    metric specified by the execution plan.

    Planned metric:
        transactions.revenue

    Generated SQL:
        SUM(transactions.customer_id)

    This must be rejected.
    """

    execution_plan = create_execution_plan()

    sql = """
    SELECT
        c.country,
        SUM(t.customer_id) AS revenue_sum
    FROM customers c
    JOIN transactions t
        ON c.customer_id = t.customer_id
    GROUP BY c.country;
    """

    try:
        validate_sql(
            sql=sql,
            database_schema=DATABASE_SCHEMA,
            execution_plan=execution_plan,
        )

    except SQLValidationError:
        print("PASS: wrong metric rejected")
        return

    raise AssertionError(
        "Validator accepted SQL using the wrong metric."
    )


def test_unknown_column():
    """
    SQL references a column that does not exist
    in the database schema.
    """

    execution_plan = create_execution_plan()

    sql = """
    SELECT
        c.country,
        SUM(t.profit) AS revenue_sum
    FROM customers c
    JOIN transactions t
        ON c.customer_id = t.customer_id
    GROUP BY c.country;
    """

    try:
        validate_sql(
            sql=sql,
            database_schema=DATABASE_SCHEMA,
            execution_plan=execution_plan,
        )

    except SQLValidationError:
        print("PASS: unknown column rejected")
        return

    raise AssertionError(
        "Validator accepted SQL containing an unknown column."
    )


def test_unknown_table():
    """
    SQL references a table that does not exist
    in the database schema.
    """

    execution_plan = create_execution_plan()

    sql = """
    SELECT
        c.country,
        SUM(p.revenue) AS revenue_sum
    FROM customers c
    JOIN payments p
        ON c.customer_id = p.customer_id
    GROUP BY c.country;
    """

    try:
        validate_sql(
            sql=sql,
            database_schema=DATABASE_SCHEMA,
            execution_plan=execution_plan,
        )

    except SQLValidationError:
        print("PASS: unknown table rejected")
        return

    raise AssertionError(
        "Validator accepted SQL containing an unknown table."
    )


def test_non_select_sql():
    """Non-SELECT statements must be rejected."""

    execution_plan = create_execution_plan()

    sql = """
    DELETE FROM transactions;
    """

    try:
        validate_sql(
            sql=sql,
            database_schema=DATABASE_SCHEMA,
            execution_plan=execution_plan,
        )

    except SQLValidationError:
        print("PASS: non-SELECT SQL rejected")
        return

    raise AssertionError(
        "Validator accepted a non-SELECT statement."
    )


def test_multiple_statements():
    """Multiple SQL statements must be rejected."""

    execution_plan = create_execution_plan()

    sql = """
    SELECT *
    FROM customers;

    DELETE FROM transactions;
    """

    try:
        validate_sql(
            sql=sql,
            database_schema=DATABASE_SCHEMA,
            execution_plan=execution_plan,
        )

    except SQLValidationError:
        print("PASS: multiple statements rejected")
        return

    raise AssertionError(
        "Validator accepted multiple SQL statements."
    )


def main():
    print("Running SQL Validator tests...\n")

    test_valid_sql()
    test_wrong_metric()
    test_unknown_column()
    test_unknown_table()
    test_non_select_sql()
    test_multiple_statements()

    print("\nAll SQL Validator tests passed.")


if __name__ == "__main__":
    main()