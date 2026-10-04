from src.query.sql.sql_executor import execute_sql


def main():
    print("Testing SQL executor...")

    sql = """
    SELECT COUNT(*) AS total_rows
    FROM customers
    """

    result = execute_sql(sql)

    print("\nQuery:")
    print(sql.strip())

    print("\nResult:")
    print(result)

    assert isinstance(result, list)
    assert len(result) == 1
    assert "total_rows" in result[0]
    assert result[0]["total_rows"] > 0

    print("\nSQL executor test passed.")


if __name__ == "__main__":
    main()