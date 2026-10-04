"""
NEXA End-to-End Query Pipeline Test

Run from project root:

    python -m tests.test_pipeline
"""

import time


def main():
    print("=" * 70, flush=True)
    print("NEXA REAL END-TO-END QUERY PIPELINE TEST", flush=True)
    print("=" * 70, flush=True)

    # ---------------------------------------------------------
    # Import query pipeline
    # ---------------------------------------------------------

    print("\n[1] Importing query pipeline...", flush=True)

    import_start = time.perf_counter()

    from src.query.pipeline import run_query
    from src.query.sql.sql_executor import execute_sql

    import_time = time.perf_counter() - import_start

    print(
        f"[IMPORT] {import_time:.3f} seconds",
        flush=True,
    )

    # ---------------------------------------------------------
    # Query
    # ---------------------------------------------------------

    query = "Show the total revenue by country."

    print("\n[2] Natural-language query", flush=True)
    print("-" * 70, flush=True)
    print(query, flush=True)

    # ---------------------------------------------------------
    # Run query pipeline
    # ---------------------------------------------------------

    print("\n[3] Running query pipeline...", flush=True)
    print("-" * 70, flush=True)

    pipeline_start = time.perf_counter()

    sql = run_query(
        query=query,
        execute=False,
    )

    pipeline_time = time.perf_counter() - pipeline_start

    # ---------------------------------------------------------
    # Display SQL
    # ---------------------------------------------------------

    print("\n[4] Validated SQL", flush=True)
    print("-" * 70, flush=True)
    print(sql, flush=True)

    print(
        f"\nPipeline time: {pipeline_time:.3f} seconds",
        flush=True,
    )

    # ---------------------------------------------------------
    # Verify generated SQL
    # ---------------------------------------------------------

    normalized_sql = " ".join(
        sql.lower().split()
    )

    assert "select" in normalized_sql
    assert "country" in normalized_sql
    assert "revenue" in normalized_sql
    assert "sum" in normalized_sql
    assert "group by" in normalized_sql

    print(
        "\n[PASS] Generated SQL contains the expected "
        "query structure.",
        flush=True,
    )

    # ---------------------------------------------------------
    # Execute validated SQL
    # ---------------------------------------------------------

    print("\n[5] Executing validated SQL...", flush=True)
    print("-" * 70, flush=True)

    execution_start = time.perf_counter()

    result = execute_sql(sql)

    execution_time = time.perf_counter() - execution_start

    # ---------------------------------------------------------
    # Display result
    # ---------------------------------------------------------

    print("\n[6] Actual database result", flush=True)
    print("-" * 70, flush=True)

    for row in result:
        print(row, flush=True)

    # ---------------------------------------------------------
    # Verify result
    # ---------------------------------------------------------

    assert isinstance(result, list)
    assert len(result) > 0

    print(
        "\n[PASS] SQL execution returned database results.",
        flush=True,
    )

    # ---------------------------------------------------------
    # Final timing
    # ---------------------------------------------------------

    total_time = pipeline_time + execution_time

    print("\n" + "=" * 70, flush=True)
    print("TIMING SUMMARY", flush=True)
    print("=" * 70, flush=True)

    print(
        f"Import time     : {import_time:.3f} seconds",
        flush=True,
    )

    print(
        f"Query pipeline  : {pipeline_time:.3f} seconds",
        flush=True,
    )

    print(
        f"SQL execution   : {execution_time:.3f} seconds",
        flush=True,
    )

    print(
        f"Total           : {total_time:.3f} seconds",
        flush=True,
    )

    print("=" * 70, flush=True)

    print(
        "\nNEXA END-TO-END PIPELINE TEST PASSED.",
        flush=True,
    )


# -------------------------------------------------------------
# IMPORTANT:
# This makes `python -m tests.test_pipeline` execute main().
# -------------------------------------------------------------

if __name__ == "__main__":
    main()