from src.analysis.tools.descriptive_statistics import (
    descriptive_statistics,
)


def test_descriptive_statistics():
    rows = [
        {"revenue": 100.0},
        {"revenue": 200.0},
        {"revenue": 300.0},
        {"revenue": 400.0},
        {"revenue": 500.0},
    ]

    result = descriptive_statistics(
        rows=rows,
        metric="revenue",
    )

    print("\n" + "=" * 70)
    print("DESCRIPTIVE STATISTICS RESULT")
    print("=" * 70)

    print("\nSummary:")
    print(result.summary)

    print("\nStatistics:")

    for key, value in result.data.items():
        print(f"{key}: {value}")

    print("=" * 70)

    assert result.tool_name == "descriptive_statistics"

    assert result.data["metric"] == "revenue"
    assert result.data["count"] == 5
    assert result.data["sum"] == 1500.0
    assert result.data["mean"] == 300.0
    assert result.data["median"] == 300.0
    assert result.data["minimum"] == 100.0
    assert result.data["maximum"] == 500.0

    assert result.source_columns == ["revenue"]
    assert result.row_count == 5

    print("TEST PASSED")


if __name__ == "__main__":
    test_descriptive_statistics()