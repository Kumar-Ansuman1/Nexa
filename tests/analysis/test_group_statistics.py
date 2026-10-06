from src.analysis.tools.group_statistics import (
    group_statistics,
)


def test_group_statistics():
    rows = [
        {
            "country": "India",
            "revenue": 100.0,
        },
        {
            "country": "India",
            "revenue": 200.0,
        },
        {
            "country": "India",
            "revenue": 300.0,
        },
        {
            "country": "USA",
            "revenue": 400.0,
        },
        {
            "country": "USA",
            "revenue": 600.0,
        },
    ]

    result = group_statistics(
        rows=rows,
        metric="revenue",
        dimension="country",
    )

    print("\n" + "=" * 70)
    print("GROUP STATISTICS RESULT")
    print("=" * 70)

    print("\nSummary:")
    print(result.summary)

    print("\nGroups:")

    for group, statistics in result.data["groups"].items():
        print(f"\n{group}")

        for key, value in statistics.items():
            print(f"  {key}: {value}")

    print("=" * 70)

    india = result.data["groups"]["India"]
    usa = result.data["groups"]["USA"]

    assert result.tool_name == "group_statistics"

    assert india["count"] == 3
    assert india["sum"] == 600.0
    assert india["mean"] == 200.0
    assert india["median"] == 200.0
    assert india["minimum"] == 100.0
    assert india["maximum"] == 300.0

    assert usa["count"] == 2
    assert usa["sum"] == 1000.0
    assert usa["mean"] == 500.0
    assert usa["median"] == 500.0
    assert usa["minimum"] == 400.0
    assert usa["maximum"] == 600.0

    assert result.source_columns == [
        "country",
        "revenue",
    ]

    assert result.row_count == 5

    print("TEST PASSED")


if __name__ == "__main__":
    test_group_statistics()