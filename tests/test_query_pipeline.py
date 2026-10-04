from src.query.pipeline import run_query


def test_query_pipeline_from_database():
    query = "Show the total revenue by country."

    result = run_query(
        query=query,
        execute=True,
    )

    print("\n" + "=" * 70)
    print("FINAL QUERY RESULT")
    print("=" * 70)

    for row in result:
        print(row)

    assert isinstance(result, list)
    assert len(result) > 0

    print("=" * 70)
    print("TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    test_query_pipeline_from_database()